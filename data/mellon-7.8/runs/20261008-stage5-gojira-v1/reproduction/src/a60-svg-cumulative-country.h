/** @file
 * @brief Country-only cumulative resolution maps with fitted CK viewports.
 */
// Copyright (c) 2026 Benjamin De Kosnik <b.dekosnik@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later
#ifndef a60_SVG_CUMULATIVE_COUNTRY_H
#define a60_SVG_CUMULATIVE_COUNTRY_H 1

#include "a60-svg-collection.h"
#include "a60-json.h"
#include <filesystem>
#include <iomanip>
#include <map>
#include <numeric>

namespace a60::country_detail {
using xy = std::pair<double, double>;
using ring = std::vector<xy>;
using polygon = std::vector<ring>;

inline string quote(const string& value)
{
  rj::StringBuffer b; rj::Writer<rj::StringBuffer> w(b);
  w.String(value.c_str()); return b.GetString();
}
inline string number(double v)
{ std::ostringstream s; s << std::setprecision(12) << v; return s.str(); }
inline string normalize_iso3(string value)
{
  const auto first = value.find_first_not_of(" \t\r\n");
  if (first == string::npos) throw std::invalid_argument("empty country code");
  value = value.substr(first, value.find_last_not_of(" \t\r\n") - first + 1);
  if (value.size() != 3) throw std::invalid_argument("country requires ISO3: " + value);
  for (char& c : value)
    {
      if (c >= 'a' && c <= 'z') c -= 'a' - 'A';
      if (c < 'A' || c > 'Z') throw std::invalid_argument("invalid ISO3: " + value);
    }
  return value;
}
inline strings validate_requests(const strings& requested, const string& boundary,
                                 const string& registry)
{
  const auto iso = deserialize_json_to_dom(registry);
  const auto geo = deserialize_json_to_dom_object(boundary);
  if (!iso.IsArray() || !geo.HasMember("countries") || !geo["countries"].IsArray())
    throw std::invalid_argument("invalid ISO registry or country boundary asset");
  strings result;
  for (const auto& input : requested)
    {
      const string code = normalize_iso3(input);
      bool valid = false, mapped = false;
      for (const auto& row : iso.GetArray())
        if (row.HasMember("alpha-3") && code == row["alpha-3"].GetString()) valid = true;
      for (const auto& row : geo["countries"].GetArray())
        if (code == row["iso3"].GetString()) mapped = true;
      if (!valid) throw std::invalid_argument("unregistered ISO3: " + code);
      if (!mapped) throw std::invalid_argument("valid ISO3 has no country geometry: " + code);
      if (std::find(result.begin(),result.end(),code) == result.end()) result.push_back(code);
    }
  return result;
}
inline string panel_id(const string& country, double lat, double lon)
{
  if (country == "JPN")
    {
      if (lat >= 30 && lat <= 47 && lon >= 128 && lon <= 147) return "main";
      if (lat >= 24 && lat < 30 && lon >= 122 && lon <= 132) return "ryukyu";
      if (lat >= 20 && lat < 30 && lon >= 132 && lon <= 155) return "pacific-islands";
      return "other";
    }
  if (country == "USA")
    {
      if (lat >= 50 && (lon < -129 || lon > 170))
        return lon > 0 ? "aleutians" : "alaska";
      if (lat < 30 && lat > 15 && lon < -130) return "hawaii";
      if (lat >= 24 && lat < 50 && lon >= -126 && lon <= -66) return "main";
      return "other";
    }
  if (country == "AUS")
    {
      if (lat >= -44 && lat <= -9 && lon >= 112 && lon <= 154) return "main";
      // Preserve offshore islands without fitting the mainland across the
      // registered 159-degree projection interruption (including Macquarie).
      return lon < 159 ? "offshore-west" : "offshore-east";
    }
  return "main";
}
inline string resolution_group(resolution_mode r)
{
  if (r == resolution_mode::r1080p || r == resolution_mode::r4k) return "ge-1080p";
  if (r == resolution_mode::r720p || r == resolution_mode::rsd) return "lt-1080p";
  return "unsupported";
}

/// Copy prepared weights without rescaling, mutation, or stale summaries.
inline swarm_geos country_slice(const swarm_geos& source, const string& code,
                         const string& group = "combined", const string& panel = "",
                         const strings& members = {})
{
  swarm_geos out(static_cast<const collection&>(source), source.key_mask);
  out.datestamp = source.datestamp;
  for (size_t i = 0; i < source.members.size(); ++i)
    {
      const string g = resolution_group(source.members[i].resolution);
      if (g == "unsupported" || (group != "combined" && g != group)) continue;
      auto copy = [&](const auto& geos, const auto& weights, auto& dest,
                      auto& dw, auto& total) {
        for (const auto& [key, p] : geos)
          if ((members.empty() ? std::get<geo::country_code>(p) == code :
               std::find(members.begin(),members.end(),std::get<geo::country_code>(p))!=members.end()) &&
              (panel.empty() || panel_id(code, std::get<geo::latitude>(p),
                                        std::get<geo::longitude>(p)) == panel))
            {
              dest.emplace(key,p); dw.emplace(key,weights.at(key));
              total += weights.at(key);
            }
      };
      copy(source.peer_geos[i],source.peer_weights[i],out.peer_geos[i],out.peer_weights[i],out.peer_totals[i]);
      copy(source.seed_geos[i],source.seed_weights[i],out.seed_geos[i],out.seed_weights[i],out.seed_totals[i]);
    }
  out.sort_mode = swarm_mode::peer; out.weigh();
  out.sort_by_swarm_mode_and_size(swarm_mode::peer);
  out.summarize_swarm(std::numeric_limits<uint>::max());
  return out;
}
struct bounds
{
  double x0=std::numeric_limits<double>::infinity(), y0=x0;
  double x1=-x0, y1=-x0;
  void add(xy p)
  {
    if (!std::isfinite(p.first) || !std::isfinite(p.second))
      throw std::runtime_error("nonfinite country coordinate");
    x0=std::min(x0,p.first); x1=std::max(x1,p.first);
    y0=std::min(y0,p.second); y1=std::max(y1,p.second);
  }
  double width() const { return x1-x0; }
  double height() const { return y1-y0; }
};
struct viewport
{
  double x=0,y=0,w=0,h=0,s=1,tx=0,ty=0;
  bounds b{};
  void fit(bounds content, double margin)
  {
    if (!(content.width()>0 && content.height()>0 && w>2*margin && h>2*margin))
      throw std::runtime_error("degenerate country viewport");
    const double px=.04*content.width(), py=.04*content.height();
    content.x0-=px;content.x1+=px;content.y0-=py;content.y1+=py;b=content;
    s=std::min((w-2*margin)/b.width(),(h-2*margin)/b.height());
    tx=x+(w-s*b.width())/2-s*b.x0;ty=y+(h-s*b.height())/2-s*b.y0;
  }
  xy apply(xy p) const { return {s*p.first+tx,s*p.second+ty}; }
};
struct panel
{
  string id, label;
  std::vector<polygon> polygons;
  std::vector<ring> outlines;
  bounds extent;
  viewport view;
};
/// Affine view of the registered CK coordinates; glyph units remain page units.
struct fitted_projection
{
  carto::ckproj source;
  viewport view;
  carto::frame pframe{source.pframe};
  point_2t meridians_to_point_2d(double lat, double lon) const
  {
    auto [x,y]=source.meridians_to_point_2d(lat,lon);
    auto [px,py]=view.apply({x,y});return {px,py};
  }
};
/// Route the unchanged audit text layer through the same fitted country panels.
struct panel_projection
{
  carto::ckproj source;
  const std::vector<panel>& panels;
  string country;
  carto::frame pframe{source.pframe};
  point_2t meridians_to_point_2d(double lat, double lon) const
  {
    const string id=panel_id(country,lat,lon);
    const auto p=std::find_if(panels.begin(),panels.end(),
                            [&](const auto& item){return item.id==id;});
    if(p==panels.end())throw std::runtime_error("missing country label panel: "+id);
    auto [x,y]=source.meridians_to_point_2d(lat,lon);
    auto [px,py]=p->view.apply({x,y});return {px,py};
  }
};
inline uint64_t total(const vul& values)
{ return std::accumulate(values.begin(), values.end(), uint64_t{0}); }
inline string rect(double x,double y,double w,double h,const string& fill)
{
  return "<rect x=\""+number(x)+"\" y=\""+number(y)+"\" width=\""+number(w)+
    "\" height=\""+number(h)+"\" fill=\""+fill+"\"/>";
}
inline void text(svg::svg_element& obj,double x,double y,const string& value,int size=38)
{
  obj.add_raw("<text x=\""+number(x)+"\" y=\""+number(y)+"\" font-family=\"DejaVu Sans,sans-serif\" font-size=\""+
              std::to_string(size)+"\" fill=\"black\">"+svg::escape_xml_attribute(value)+"</text>");
}
}

namespace a60 {
class cumulative_map_renderer
{
  const swarm_geos& source;
  carto::ckproj projection;
  string output;
  rj::Document boundaries;
  render_state state;
  double radius_base = 2.6;
  strings requested_countries;
  string input_mode;
  std::map<string,strings> regions;
  std::map<string,string> region_names;
  rj::Document map_style;
  using panel = country_detail::panel;
  using xy = country_detail::xy;

  bool contains(const string& selector,const string& code) const
  {
    if (!regions.contains(selector)) return selector==code;
    const auto& codes=regions.at(selector);
    return std::find(codes.begin(),codes.end(),code)!=codes.end();
  }
  swarm_geos slice(const string& code,const string& group="combined",const string& panel="") const
  { return country_detail::country_slice(source,code,group,panel,regions.contains(code)?regions.at(code):strings{}); }

  xy project(double lon,double lat) const
  { auto [x,y]=projection.meridians_to_point_2d(lat,lon);return {x,y}; }

  std::vector<panel> panels_for(const string& code,const swarm_geos& selected)
  {
    using namespace country_detail;
    std::map<string,panel> panels;
    auto ensure=[&](const string& id)->panel& {
      auto& p=panels[id];p.id=id;
      p.label=id=="main" ? (code=="USA"?"Contiguous USA":code=="AUS"?"Mainland and Tasmania":code=="JPN"?"Main islands":"") :
        id=="alaska"?"Alaska":id=="hawaii"?"Hawaii":id=="aleutians"?"Western Aleutians":
        id=="ryukyu"?"Ryukyu islands":id=="pacific-islands"?"Pacific islands":
        code=="AUS"?"Offshore islands":"Other "+code+"-coded locations";
      return p;
    };
    for (const auto& c : boundaries["countries"].GetArray())
      if (contains(code,c["iso3"].GetString()))
        for (const auto& coordinates : c["geometry"]["coordinates"].GetArray())
          {
            double lon=0,lat=0;size_t n=coordinates[0].Size();
            for (const auto& v : coordinates[0].GetArray()) { lon+=v[0].GetDouble();lat+=v[1].GetDouble(); }
            auto& p=ensure(panel_id(code,lat/n,lon/n));
            country_detail::polygon poly;
            for (const auto& r : coordinates.GetArray())
              {
                ring path;
                for (const auto& v : r.GetArray())
                  { auto point=project(v[0].GetDouble(),v[1].GetDouble());path.push_back(point);p.extent.add(point); }
                // Clipped polygon edges close the fill, but are not borders.
                ring outline;
                for (rj::SizeType j=1;j<r.Size();++j)
                  {
                    const double a=r[j-1][0].GetDouble(),b=r[j][0].GetDouble();
                    bool seam=false;
                    for (double cut : {-180.,-111.,-21.,69.,159.,180.})
                      if (std::abs(a-cut)<1e-7 && std::abs(b-cut)<1e-7) seam=true;
                    if (seam)
                      { if(outline.size()>1)p.outlines.push_back(outline);outline.clear(); }
                    else
                      { if(outline.empty())outline.push_back(path[j-1]);outline.push_back(path[j]); }
                  }
                if(outline.size()>1)p.outlines.push_back(outline);
                poly.push_back(std::move(path));
              }
            p.polygons.push_back(std::move(poly));
          }
    // Account for all selected observations; code membership controls inclusion.
    for (const auto* geos : {&selected.peer_geos,&selected.seed_geos})
      for (const auto& member : *geos)
        for (const auto& [key,gp] : member)
          {
            static_cast<void>(key);
            const double lat=std::get<geo::latitude>(gp),lon=std::get<geo::longitude>(gp);
            ensure(panel_id(code,lat,lon)).extent.add(project(lon,lat));
          }
    // A paired render supplies the union of both works' observed coordinates.
    // Including these before fitting makes the transforms identical.
    if (map_style.IsObject() && map_style.HasMember("frame_points") && map_style["frame_points"].HasMember(code.c_str()))
      for (const auto& p:map_style["frame_points"][code.c_str()].GetArray())
        ensure(panel_id(code,p[1].GetDouble(),p[0].GetDouble())).extent.add(project(p[0].GetDouble(),p[1].GetDouble()));
    std::vector<panel> result;
    for (const string id : {"main","alaska","hawaii","aleutians","offshore-west","offshore-east","ryukyu","pacific-islands","other"})
      if (panels.contains(id)) result.push_back(panels.at(id));
    if (result.empty()) throw std::runtime_error("no country geometry: "+code);
    // A single observation without polygon coverage needs a nondegenerate inset.
    for (auto& p : result)
      {
        if (p.extent.width()==0) { p.extent.x0-=1;p.extent.x1+=1; }
        if (p.extent.height()==0) { p.extent.y0-=1;p.extent.y1+=1; }
      }
    return result;
  }

public:
  cumulative_map_renderer(const swarm_geos& input,const carto::cartography<carto::ckproj>& cartog,
                          const string& odir,const string& boundary,const strings& countries,
                          const string& mode = "sample-cache-cumulative",
                          const string& region_file = "",const string& style_file = "")
    : source(input),projection(cartog.p),output(odir),boundaries(deserialize_json_to_dom_object(boundary)),requested_countries(countries),input_mode(mode)
  {
    if (!region_file.empty()) {
      const auto definitions=deserialize_json_to_dom_object(region_file);
      for (const auto& r:definitions["regions"].GetArray()) {
        const string id=r["id"].GetString();
        region_names[id]=r["name"].GetString();
        for(const auto& c:r["country_codes"].GetArray())regions[id].push_back(c.GetString());
      }
    }
    if (!style_file.empty())map_style=deserialize_json_to_dom_object(style_file);
    if(input_mode!="sample-cache-cumulative" && input_mode!="cumulative-geojson")
      throw std::invalid_argument("unsupported country input mode: "+input_mode);
    state.weigh=true;state.opacity=.05;
    set_select(state.visible_mode,svg::select::vector|svg::select::text);
    svg::active_spectrum()=svg::izzi_hue_palette;
    initialize_colors(source,state,false);
    uint64_t maximum=0;
    for (size_t i=0;i<source.members.size();++i)
      for (const auto& [key,p] : source.peer_geos[i])
        if (std::any_of(countries.begin(),countries.end(),[&](const auto& code){return contains(code,std::get<geo::country_code>(p));}))
          maximum=std::max(maximum,uint64_t(source.peer_weights[i].at(key)));
    // One shared coefficient for this entire invocation: fit even large bubbles.
    if (maximum) radius_base=std::min(2.6,180.0/std::sqrt(double(maximum)));
    if (map_style.IsObject() && map_style.HasMember("radius_base")) {
      const double fixed=map_style["radius_base"].GetDouble();
      // JSON receipts retain 15 significant digits; tolerate round-trip noise.
      if (!(fixed>0 && fixed<=radius_base*(1.0+1e-12)))throw std::invalid_argument("shared radius exceeds safe native coefficient");
      radius_base=fixed;
    }
  }

  /// Reference reduction directly over the prepared worldwide source, before
  /// country_slice, partitioning or rendering. Contains no IP addresses.
  void write_source_accounting() const
  {
    using namespace country_detail;
    const string stem=source.cache_match.empty()?source.match:source.cache_match;
    std::ofstream file(output+stem+"-country-source-accounting.json");
    file<<std::setprecision(15)<<"{\"schema\":\"alpha60-country-source-accounting/1\",\"input_mode\":"<<quote(input_mode)
      <<",\"dates\":"<<quote(source.datestamp)<<",\"members\":[";
    std::map<string,std::set<xy>> coordinates;
    for(size_t i=0;i<source.members.size();++i)
      {
        if(i)file<<',';
        file<<"{\"name\":"<<quote(source.members[i].name)<<",\"id\":"<<source.members[i].tid
          <<",\"resolution\":"<<quote(a60::to_string(source.members[i].resolution))
          <<",\"group\":"<<quote(resolution_group(source.members[i].resolution))
          <<",\"color\":"<<quote(svg::to_string(state.get_color(source.members[i].name)))
          <<",\"downloaders\":"<<source.peer_totals[i]<<",\"uploaders\":"<<source.seed_totals[i]<<",\"countries\":{";
        bool first=true;
        for(const string& code:requested_countries)
          {
            uint64_t peers=0,seeds=0;
            auto sum=[&](const auto& geos,const auto& weights,uint64_t& result) {
              for(const auto& [key,point]:geos)
                if(contains(code,std::get<geo::country_code>(point)))
                  {
                    result+=weights.at(key);
                    coordinates[code].emplace(std::get<geo::longitude>(point),std::get<geo::latitude>(point));
                  }
            };
            sum(source.peer_geos[i],source.peer_weights[i],peers);
            sum(source.seed_geos[i],source.seed_weights[i],seeds);
            if(!first)file<<',';
            first=false;
            file<<quote(code)<<":{\"downloaders\":"<<peers<<",\"uploaders\":"<<seeds<<'}';
          }
        uint64_t unlocated_peers=0,unlocated_seeds=0;
        for(const auto& [key,gp]:source.peer_geos[i])if(geo::is_on_null_island(gp))unlocated_peers+=source.peer_weights[i].at(key);
        for(const auto& [key,gp]:source.seed_geos[i])if(geo::is_on_null_island(gp))unlocated_seeds+=source.seed_weights[i].at(key);
        file<<"},\"unlocated\":{\"downloaders\":"<<unlocated_peers<<",\"uploaders\":"<<unlocated_seeds<<"}}";
      }
    file<<"],\"country_coordinates\":{";
    bool first=true;
    for(const string& code:requested_countries)
      {
        if(!first)file<<',';
        first=false;
        file<<quote(code)<<":[";bool firstpoint=true;
        for(const auto& [lon,lat]:coordinates[code])
          { if(!firstpoint)file<<',';firstpoint=false;file<<'['<<lon<<','<<lat<<']'; }
        file<<']';
      }
    file<<"}}\n";
    if(!file)throw std::runtime_error("failed country source accounting write");
  }

  void render_cumulative_maps_by_country(string iso3)
  {
    using namespace country_detail;
    if (!regions.contains(iso3))iso3=normalize_iso3(iso3);
    if (std::find(requested_countries.begin(),requested_countries.end(),iso3)==requested_countries.end())
      throw std::invalid_argument("country was not validated for this context: "+iso3);
    string country;
    if (region_names.contains(iso3))country=region_names.at(iso3);
    for (const auto& c : boundaries["countries"].GetArray())
      if (iso3==c["iso3"].GetString()) country=c["name"].GetString();
    if (country.empty()) throw std::invalid_argument("no boundary for "+iso3);
    const swarm_geos selected=slice(iso3);
    auto panels=panels_for(iso3,selected);
    const double margin=210;
    auto layout=[&](double width,double height) {
      auto pp=panels;
      const double insets=pp.size()>1 ? height*.28 : 0;
      pp[0].view={60,230,width-120,height-450-insets};
      pp[0].view.fit(pp[0].extent,margin);
      if (pp.size()>1)
        for (size_t i=1;i<pp.size();++i)
          {
            const double pw=(width-120)/(pp.size()-1);
            pp[i].view={60+pw*(i-1),height-210-insets,pw-20,insets-50};
            pp[i].view.fit(pp[i].extent, std::min(210.0,std::min(pw-20,insets-50)*.22));
          }
      return pp;
    };
    auto landscape=layout(4224,2112),portrait=layout(2112,4224);
    double width=4224,height=2112;
    if (portrait[0].view.s>landscape[0].view.s) { width=2112;height=4224;panels=portrait; }
    else panels=landscape;
    if (iso3=="JPN") {
      auto square=layout(3000,3000);
      if(square[0].view.s>panels[0].view.s){width=3000;height=3000;panels=square;}
    }
    // Exact same transforms in every partition. Increase inset padding to contain
    // actual panel radii while retaining the shared area coefficient.
    for (size_t i=1;i<panels.size();++i)
      {
        auto sub=slice(iso3,"combined",panels[i].id);double maxr=0;
        for (const auto& weights:sub.peer_weights)
          for (const auto& [key,w]:weights) { static_cast<void>(key);maxr=std::max(maxr,radius_base*std::sqrt(double(w))); }
        panels[i].view.fit(panels[i].extent,map_style.IsObject()?192.0:std::max(32.0,maxr+12));
      }
    string lower=iso3;for(char& c:lower)if(c>='A' && c<='Z')c+='a'-'A';
    const string stem=source.cache_match.empty()?source.match:source.cache_match;
    std::ostringstream receipt;receipt<<std::setprecision(15);
    receipt<<"{\"schema\":\"alpha60-country-render/1\",\"input_mode\":"<<quote(input_mode)<<",\"country\":"<<quote(iso3)
      <<",\"name\":"<<quote(country)<<",\"collection\":"<<quote(stem)
      <<",\"dates\":"<<quote(source.datestamp)<<",\"page\":["<<width<<','<<height<<"]"
      <<",\"radius_base\":"<<radius_base<<",\"opacity\":0.05,\"panels\":[";
    for (size_t i=0;i<panels.size();++i)
      {
        const auto& p=panels[i];const auto& v=p.view;if(i)receipt<<',';
        auto sub=slice(iso3,"combined",p.id);
        receipt<<"{\"id\":"<<quote(p.id)<<",\"label\":"<<quote(p.label)
          <<",\"scale\":"<<v.s<<",\"translate\":["<<v.tx<<','<<v.ty<<"]"
          <<",\"rect\":["<<v.x<<','<<v.y<<','<<v.w<<','<<v.h<<"]"
          <<",\"bounds\":["<<v.b.x0<<','<<v.b.y0<<','<<v.b.x1<<','<<v.b.y1<<"]"
          <<",\"downloaders\":"<<total(sub.peer_totals)<<",\"uploaders\":"<<total(sub.seed_totals)<<'}';
      }
    receipt<<"],\"variants\":[";
    bool first=true;
    for (const string group : {"combined","ge-1080p","lt-1080p"})
      {
        auto selected_group=this->slice(iso3,group);
        auto& slice=selected_group;
        const uint64_t peers=total(slice.peer_totals),seeds=total(slice.seed_totals);
        const string name=stem+"-data-country-"+lower+"-"+group;
        if(!first)receipt<<',';
        first=false;
        receipt<<"{\"group\":"<<quote(group)<<",\"file\":"<<quote(name+".svg")
          <<",\"downloaders\":"<<peers<<",\"uploaders\":"<<seeds
          <<",\"status\":"<<quote(peers?"rendered":"no-downloader-data")<<",\"members\":[";
        for(size_t i=0;i<slice.members.size();++i)
          {
            if(i)receipt<<',';
            receipt<<"{\"name\":"<<quote(slice.members[i].name)<<",\"id\":"<<slice.members[i].tid
              <<",\"color\":"<<quote(svg::to_string(state.get_color(slice.members[i].name)))
              <<",\"downloaders\":"<<slice.peer_totals[i]<<",\"uploaders\":"<<slice.seed_totals[i]<<'}';
          }
        receipt<<"],\"cities\":[";bool cityfirst=true;
        for(const auto& wp:slice.sum_wkeys)
          {
            const auto& gp=slice.sum_geos.at(std::get<1>(wp));
            if(!cityfirst)receipt<<',';
            cityfirst=false;
            receipt<<"{\"key\":"<<quote(std::get<1>(wp))<<",\"city\":"<<quote(std::get<geo::city>(gp))
              <<",\"downloaders\":"<<std::get<0>(wp)<<",\"coordinates\":["<<std::get<geo::longitude>(gp)<<','<<std::get<geo::latitude>(gp)<<"]}";
          }
        receipt<<"],\"labels\":[";
        if(!peers) { receipt<<"]}";continue; }
        svg::svg_element obj(output+name,svg::area<>{width,height});
        obj.add_raw(rect(0,0,width,height,"white"));
        obj.add_desc(country+" cumulative downloader map; "+group+"; "+source.datestamp);
        text(obj,70,85,country+" · "+source.name,64);
        text(obj,70,151,stem+" · "+group+" · "+source.datestamp,34);
        text(obj,70,196,"Cumulative downloader weights · "+std::to_string(peers)+" · registered Cahill–Keyes",30);
        for(const auto& p:panels)
          {
            const auto& v=p.view;
            obj.add_raw(rect(v.x,v.y,v.w,v.h,"#f2f2f2"));
            for(const auto& poly:p.polygons)
              {
                std::ostringstream path;
                for(const auto& r:poly)
                  {
                    bool initial=true;
                    for(const auto& pt:r)
                      { auto [x,y]=v.apply(pt);path<<(initial?'M':'L')<<number(x)<<' '<<number(y)<<' ';initial=false; }
                    path<<"Z ";
                  }
                obj.add_raw("<path d=\""+path.str()+"\" fill=\"white\" fill-rule=\"evenodd\" stroke=\"none\"/>");
              }
            std::ostringstream border;
            for(const auto& line:p.outlines)
              {
                bool initial=true;
                for(const auto& point:line)
                  { auto [x,y]=v.apply(point);border<<(initial?'M':'L')<<number(x)<<' '<<number(y)<<' ';initial=false; }
              }
            obj.add_raw("<path d=\""+border.str()+"\" fill=\"none\" stroke=\"#777\" stroke-width=\"1.1\"/>");
            if(!p.label.empty())text(obj,v.x+16,v.y+40,p.label,32);
            auto sub=this->slice(iso3,group,p.id);
            carto::cartography<fitted_projection> view(carto::frame(svg::area<>{width,height}),{projection,v});
            obj.add_raw("<g data-country=\""+iso3+"\" data-panel=\""+p.id+"\" data-group=\""+group+"\">");
            augment_ccollection_vector_cloud(obj,sub,view,state,radius_base,iso3+"-"+p.id+"-");
            obj.add_raw("</g>");
          }
        // Reuse the existing cumulative-audit label style verbatim: centered
        // Apercu, weight-scaled black text with white outline at the location.
        // Reference: all-you-need-is-kill-data-ge-1080p-4k.webp. No callouts.
        carto::cartography<panel_projection> label_view(
          carto::frame(svg::area<>{width,height}),{projection,panels,iso3});
        augment_ccollection_text(obj,slice,label_view,state,10,1,true);
        geo::swgeoi_peers ranked;
        for(const auto& wp:slice.sum_wkeys)
          ranked.insert(std::make_tuple(uint(std::get<0>(wp)),slice.sum_geos.at(std::get<1>(wp))));
        size_t rank=0;bool label_first=true;
        for(const auto& [weight,gp]:ranked)
          {
            if(weight<1 || rank++>=10)break;
            const string city=std::get<geo::city>(gp);
            const bool placed=!city.empty() && !geo::is_on_null_island(gp);
            const double lat=std::get<geo::latitude>(gp),lon=std::get<geo::longitude>(gp);
            if(!label_first)receipt<<',';
            label_first=false;
            receipt<<"{\"city\":"<<quote(city)<<",\"weight\":"<<weight
              <<",\"placed\":"<<(placed?"true":"false");
            if(placed)
              {
                auto [x,y]=label_view.to_point_2d(lat,lon);
                receipt<<",\"position\":["<<x<<','<<y<<']';
              }
            receipt<<'}';
          }
        text(obj,70,height-148,"Member colors: 2160 yellow/orange · 1080 pink/purple · 720 blue · SD green",30);
        text(obj,70,height-105,"Circle area ∝ downloader weight; shared radius coefficient "+number(radius_base)+"; opacity 5%",28);
        text(obj,70,height-64,(input_mode=="sample-cache-cumulative"
          ? "Natural Earth 1:10m · country-code selection · cumulative sample-cache counts; no product rescaling"
          : "Natural Earth 1:10m · country-code selection · cumulative GeoJSON; worldwide member rescaling"),26);
        if(panels.size()>1)text(obj,70,height-25,"Insets have independent geographic scales; circle weight scale is identical in every panel.",26);
        receipt<<"]}";
      }
    receipt<<"]}\n";
    std::ofstream file(output+stem+"-data-country-"+lower+".json");file<<receipt.str();
    if(!file)throw std::runtime_error("failed country receipt write");
  }
};
}
#endif
