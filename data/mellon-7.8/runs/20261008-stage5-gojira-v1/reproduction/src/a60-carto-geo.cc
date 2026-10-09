// alpha60 torrent carto geographic checks -*- mode: C++ -*-

// alpha60
// bittorrent x scrape x data + analytics

// Copyright (c) 2016-2026, Benjamin De Kosnik <b.dekosnik@gmail.com>

// This file is part of the alpha60 library.  This library is free
// software; you can redistribute it and/or modify it under the terms
// of the GNU General Public License as published by the Free Software
// Foundation; either version 3, or (at your option) any later
// version.

// This library is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.

#include "a60.h"
#include "a60-svg-carto-geo.h"
#include "a60-btiha-geojson.h"
#include "a60-collection-coalesce-synthetic.h"
#include "a60-collection-objects-factory.h"
#include "a60-quiet.h"
#include "a60-svg-collection-color.h"
#include "a60-svg-cumulative-country.h"


using namespace a60;


string
usage()
{
  string s("usage:\n");
  s += "  a60-carto-geo.exe [--quiet] GEOJSON\n";
  s += "  a60-carto-geo.exe [--quiet] --cumulative-maps ";
  s += "CACHE_DIR COLLECTION_KEY\n";
  s += "  a60-carto-geo.exe [--quiet] --cumulative-product-maps ";
  s += "CUMULATIVE-BTIHA-GEOJSON BTIHA-METADATA-JSON COLLECTION_KEY";
  s += " [--country ISO3 ...] [--region-definition FILE] [--map-style FILE] [--country-boundaries FILE --country-iso-registry FILE]";
  s += a60::k::newline;
  return s;
}


resolution_mode
resolution_from_product(const string& value)
{
  if (value == "sd")
    return resolution_mode::rsd;
  if (value == "720")
    return resolution_mode::r720p;
  if (value == "1080")
    return resolution_mode::r1080p;
  if (value == "2160")
    return resolution_mode::r4k;
  if (value == "4320")
    return resolution_mode::r8k;
  throw std::runtime_error("unsupported published resolution: " + value);
}


encoding_mode
encoding_from_product(const string& value)
{
  if (value == "none")
    return encoding_mode::none;
  if (value == "264")
    return encoding_mode::e264;
  if (value == "265")
    return encoding_mode::e265;
  if (value == "xvid")
    return encoding_mode::exvid;
  throw std::runtime_error("unsupported published encoding: " + value);
}


/// Rebuild the exact unique-BTIH collection recorded by a published product.
collection
collection_from_btiha_product(collection cll, const string& product,
			      published_btiha_totals& totals)
{
  rj::Document dom = deserialize_json_to_dom_object(product);
  const string product_key = cll.cache_match.empty()
    ? cll.match : cll.cache_match;
  if (!dom.IsObject() || !dom.HasMember("collection_key")
      || !dom["collection_key"].IsString()
      || string(dom["collection_key"].GetString()) != product_key)
    throw std::runtime_error(
      "cumulative BTIHA metadata collection mismatch: " + product);
  const char* members_key = "collection_cumulative_by_btiha";
  if (!dom.HasMember(members_key) || !dom[members_key].IsArray())
    throw std::runtime_error(
      "cumulative BTIHA metadata member array is missing: " + product);

  cll.members.clear();
  cll.uids.clear();
  for (const auto& item : dom[members_key].GetArray())
    {
      if (!item.IsObject() || !item.HasMember("id")
	  || !item["id"].IsUint64() || !item.HasMember("name")
	  || !item["name"].IsString() || !item.HasMember("resolution")
	  || !item["resolution"].IsString() || !item.HasMember("encoding")
	  || !item["encoding"].IsString()
	  || !item.HasMember("udownloaders")
	  || !item["udownloaders"].IsUint64()
	  || !item.HasMember("uuploaders")
	  || !item["uuploaders"].IsUint64())
	throw std::runtime_error(
	  "malformed cumulative BTIHA metadata member: " + product);
      media_object member;
      member.tid = item["id"].GetUint64();
      member.name = item["name"].GetString();
      member.resolution = resolution_from_product(
	item["resolution"].GetString());
      member.encoding = encoding_from_product(item["encoding"].GetString());
      if (!cll.uids.emplace(member.name, member.tid).second)
	throw std::runtime_error(
	  "duplicate cumulative BTIHA metadata member: " + member.name);
      if (!totals.emplace(
	    member.name,
	    std::make_pair(item["udownloaders"].GetUint64(),
			   item["uuploaders"].GetUint64())).second)
	throw std::runtime_error(
	  "duplicate cumulative BTIHA metadata total: " + member.name);
      cll.members.push_back(std::move(member));
    }
  if (cll.members.empty())
    throw std::runtime_error(
      "empty cumulative BTIHA metadata member array: " + product);
  return cll;
}

void
print_geo_peer(geo::geo_peer& p)
{
  std::cout << "lat: " << std::get<geo::latitude>(p) << std::endl;
  std::cout << "long: " << std::get<geo::longitude>(p) << std::endl;
  std::cout << "country: " << std::get<geo::country>(p) << std::endl;
  std::cout << "region: " << std::get<geo::region>(p) << std::endl;
  std::cout << "city: " << std::get<geo::city>(p) << std::endl;
  std::cout << std::endl;
}


bool
pre_check_geoip_install()
{
  bool ret(false);

  if constexpr (a60::k::geolocation_state != geo::iplocation_mode::none)
    {
      // Empty meta peer representing Google DNS ip address only.
      string sgdns("8.8.8.8");
      geo::geo_peer pgoogle = geo::make_geo_peer(sgdns);
      geo::vgeo_peers peerstest;
      peerstest.push_back(pgoogle);

      // test 1
      geo::geo_peer pmmp1 = geo::make_geo_peer(sgdns);
      print_geo_peer(pmmp1);

      geo::geo_peer pmmp2 = geo::make_geo_peer(sgdns, false, true);
      print_geo_peer(pmmp2);

      /*
	ip: 114.84.162.223
	country: CHN
	lat: 31.0456
	long: 121.4
	city: 23
	region: Shanghai
      */
      string sxzh("114.84.162.223");
      geo::geo_peer pmmp3 = geo::make_geo_peer(sxzh);
      print_geo_peer(pmmp3);

      string sxipv6("::ffff:46.165.244.207");
      geo::geo_peer pmmp4 = geo::make_geo_peer(sxipv6);
      print_geo_peer(pmmp4);
    }

  return ret;
}


/// Augmentation for Network characteristics GeoJSON from swarm_features.
void
augment_swarm_features_geojson(const string geoj, const auto& cartog,
			       string odir = "./tmp/")
{
  using std::clog;
  using std::endl;
  using svg::select;
  const auto& a = cartog.f.frame_area;

  // Get name from input GeoJSON file's collection_key field.
  // NB: key is the stringified version of the H3 Hexagon id.
  rj::Document dom = deserialize_json_to_dom_object(geoj);
  string sname = to_lowercase_string(search_dom_for_string_field(dom, "id"));
  string sdstamp = search_dom_for_string_field(dom, "datestamp");

  // Deserialize geojson file into into swarm_features.
  umsfeatures gfeatures = a60::deserialize_swarm_features(geoj);
  if (gfeatures.empty())
    {
      string m("augment_swarm_features_geojson: failed, input has no GeoJSON Features.");
      m += a60::k::newline;
      m += geoj;
      m += a60::k::newline;
    }
  else
    clog << "augment_swarm_features_geojson:: found " << gfeatures.size() << endl;


  // Display min and max.
  const uint dmin = 1.5;
  const uint dmax = 150;

  // Find serialized Feature.field for sizing data range.
  using size_type = swarm_datum::size_type;
  auto lget_min_max_member = [&gfeatures](size_type swarm_datum::* mptr)
  {
    std::set<size_type> values;
    for (const auto& [key, swrmf] : gfeatures)
	values.insert(swrmf.downloaders.*mptr);
    std::tuple<size_type, size_type> ret { *values.begin(), *values.rbegin() };
    return ret;
  };

  const auto [ szmin, szmax ] = lget_min_max_member(&swarm_datum::size);
  const auto [ mzmin, mzmax ] = lget_min_max_member(&swarm_datum::mobile);
  const auto [ satmin, satmax ] = lget_min_max_member(&swarm_datum::satellite);
  const auto [ hzmin, hzmax ] = lget_min_max_member(&swarm_datum::hosting);
  const auto [ serzmin, serzmax ] = lget_min_max_member(&swarm_datum::service);


  // Start rendering.
  render_state& rs = get_render_state();
  const render_state rspre = rs;

  select vm = select::vector | select::cartography | select::text;
  set_select(rs.visible_mode, vm);

  // Make display groups for text annotations, fiber, mobile, and
  // satellite downloaders.  Doing it this way will allow data to show
  // up as separate layers in the svg.
  group_element gtxt;
  gtxt.start_element("text");
  group_element gfiber;
  gfiber.start_element("fiber");
  group_element gnet;
  // Multiply so the white halo falloff of the hosting/service rings
  // becomes neutral instead of feathering over the basemap.
  gnet.start_element("network-characteristics", svg::k::no_style,
		     "style=\"mix-blend-mode:multiply\"");
  group_element gmobile;
  gmobile.start_element("mobile");
  group_element gsat;
  gsat.start_element("satellite"); // asama orange

  const color_qi klr_lps(31,71,136); // jp lapis
  const color_qi klr_mul(59,14,75); // jp mulberry
  const color_qi klr_kgr(0,148,16); // kgreen
  const color_qi klr_r(255,29,16); // kred
  const color_qi klr_cr(220,20,60); // kcrimson
  style fstyl { klr_lps, 0.2, color::white, 0.0, 0.0 };
  style mstyl { klr_kgr, 0.2, klr_kgr, 0.0, 0.3 };
  style satstyl { klr_cr, 0.95, color::white, 1.0, 0.2 };
  typography typo = svg::k::apercu_typo;

  for (const auto& [ key, swrmf ] : gfeatures)
    {
      // Extract lat/log location, transform to display location.
      const swarm_locus& loc(swrmf.coordinates);
      const swarm_datum& dls(swrmf.downloaders);
      const point_2t cp = cartog.to_point_2d(loc.point);

      // downloaders.size
      if (dls.size)
	{
	  uint fsz = scale_value_on_range(dls.size, szmin, szmax, dmin, dmax);

	  // Style small instances as opaque, large as transparent.
	  style dlstyl(fstyl);
	  if (dls.size < szmax * 0.05)
	    dlstyl._M_fill_opacity = 1.0;
	  auto cdl = make_circle(cp, dlstyl, fsz);
	  gfiber.add_element(cdl);
	}

      // network characteristics hosting, service.
      svg_element rsvg("wrapper", a, false);
      if (dls.hosting >= hzmax * .25)
	{
	  //const uint thismax = double(hzmax) / szmax;
	  const uint thismax = double(dmax) / 3;
	  uint hsz = scale_value_on_range(dls.hosting, hzmin, hzmax, dmin, thismax);
	  point_to_ring_halo(rsvg, cp, hsz, hsz * 0.25,
			     color::darkviolet, color::white);
	  gnet.add_element(rsvg);
	}
      if (dls.service >= serzmax* .25)
	{
	  //const uint thismax = double(serzmax)/ szmax;
	  const uint thismax = double(dmax) / 3;
	  uint sersz = scale_value_on_range(dls.service, serzmin, serzmax, dmin, thismax);
	  point_to_ring_halo(rsvg, cp, sersz, sersz * 0.25,
			     color::asamapink, color::white);
	  gnet.add_element(rsvg);
	}

      // mobile
      if (dls.mobile)
	{
	  //const uint thismax = double(mzmax) / szmax;
	  const uint thismax = double(dmax) / 3;
	  uint msz = scale_value_on_range(dls.mobile, mzmin, mzmax, 2, thismax);

	  // Style small instances as outline, large as transparent.
	  style dlstyl(mstyl);
	  if (dls.mobile < szmax * 0.05)
	    {
	      msz += dmin;
	      dlstyl._M_fill_opacity = 0;
	      dlstyl._M_stroke_opacity = 1;
	    }

	  auto mdl = make_circle(cp, mstyl, msz);
	  gmobile.add_element(mdl);
	}

      // satellite
      if (dls.satellite)
	{
	  //const uint thismax = double(satmax) / szmax;
	  const uint thismax = double(dmax) / 7.5;
	  uint ssz = scale_value_on_range(dls.satellite, satmin, satmax, 2, thismax);
	  auto sdl = make_path_polygon(cp, satstyl, ssz, 3);
	  gsat.add_element(sdl);
	}

      // text (iff top n% in size) 10-50% only seoul
      // or min_max_median
      if (dls.size >= szmax * .25)
	{
	  string label = loc.city.empty() ? loc.country_code : loc.city;
	  text_element t = style_text(label, cp, typo);
	  gtxt.add_element(t);
	}
    }

  gtxt.finish_element();
  gfiber.finish_element();
  gnet.finish_element();
  gmobile.finish_element();
  gsat.finish_element();


  const string vpstr(to_string(uint(a._M_width)) + "-x-" + to_string(uint(a._M_height)));
  const string fname(sname + "-carto-" + sdstamp + "-" + vpstr);
  svg_element obj = make_map_base(odir + fname, rs, cartog);
  obj.add_element(gfiber);
  obj.add_element(gmobile);
  obj.add_element(gnet);
  obj.add_element(gsat);
  obj.add_element(gtxt);

  rs = rspre;
}


/// Debug chart of each BTIH and its assigned color, for verification of
/// the colorband assignment. One row per member in swarm order: a color
/// swatch, the BTIH name, and the hex value. Also prints a name -> color
/// table to stdout. Local verification artifact; not published.
void
augment_btiha_color_debug_chart(const swarm_geos& wcll,
				const render_state& tr,
				const string odir, const string type)
{
  const double row_height = 28;
  const double swatch = 20;
  const double margin = 30;
  const double width = 1800;
  const uint height = static_cast<uint>(margin * 2
    + (wcll.members.size() + 1) * row_height);
  const area<> afrm(width, height);

  std::ostringstream ostr;
  ostr << wcll.slice_name_mangled() << a60::k::loline << type
       << a60::k::loline << "btiha-colors-debug";
  svg_element obj = make_info_base(odir + ostr.str(), afrm);

  typography typo = svg::k::apercu_typo;
  typo._M_anchor = svg::typography::anchor::start;
  typo._M_baseline = svg::typography::baseline::middle;
  typo._M_style = svg::k::b_style;

  double row = 0;
  auto place_row = [&](const string& label, const color_qi klr)
  {
    const double y = margin + row * row_height;
    rect_element r;
    rect_element::data dr = { margin, y, swatch, swatch };
    const style sstyl = { klr, 1.0, color::black, 1.0, 0.5 };
    r.start_element();
    r.add_data(dr);
    r.add_style(sstyl);
    r.finish_element();
    obj.add_element(r);

    styled_text(obj, label, { margin + swatch + 12, y + swatch / 2 }, typo);
    ++row;
  };

  place_row("BTIH -> assigned color ("
	    + to_string(static_cast<uint>(wcll.members.size()))
	    + " members)", color::white);
  for (const auto& mrkup : wcll.members)
    {
      const color_qi klr = tr.get_color(mrkup.name);
      place_row(mrkup.name + a60::k::space + a60::k::space + to_string(klr),
		klr);
      std::cout << "btiha-color " << mrkup.name << " "
		<< to_string(klr) << std::endl;
    }
}


/// Render the two resolution partitions used by media-object audit pages.
template<typename _Proj>
void
render_cumulative_maps(swarm_geos& wcllu,
		       const carto::cartography<_Proj>& carto,
		       const string& odir,
		       const bool render_debug_colors = true)
{
  wcllu.sort_mode = swarm_mode::peer;
  wcllu.weigh();

  render_state tr;
  tr.weigh = true;
  tr.opacity = 0.05;
  set_select(tr.visible_mode,
	     select::vector | select::cartography | select::text);
  svg::active_spectrum() = svg::izzi_hue_palette;
  initialize_colors(wcllu, tr, false);

  struct partition_request
  {
    resolution_mode m1;
    resolution_mode m2;
    string type;
  };
  const std::vector<partition_request> partitions =
    {
      { resolution_mode::r1080p, resolution_mode::r4k,
	"cumulative-ge-1080p" },
      { resolution_mode::r720p, resolution_mode::rsd,
	"cumulative-lt-1080p" },
    };
  constexpr uint audit_label_topn = 10;
  constexpr uint audit_label_threshold = 1;
  for (const auto& [ m1, m2, type ] : partitions)
    {
      swarm_geos wpart = wcllu.partition_cache_by_mode(m1, m2);
      if (wpart.members.empty())
	{
	  // A media object can have no qualifying members in a resolution
	  // partition (for example, a music-only collection has no 1080p or
	  // 4K torrents).  An empty partition renders no vector clouds and
	  // therefore cannot carry the top-location label layer, so publish
	  // no slice rather than an unlabeled plate.
	  std::cout << "skip empty resolution partition: " << type
		    << std::endl;
	  continue;
	}
      wpart.sort_mode = swarm_mode::peer;
      wpart.sort_by_swarm_mode_and_size(swarm_mode::peer);
      wpart.summarize_swarm(std::numeric_limits<uint>::max());
      augment_collection(wpart, carto, odir, type, tr,
			 audit_label_topn, true, audit_label_threshold);
      if (render_debug_colors)
	augment_btiha_color_debug_chart(wpart, tr, odir, type);
    }
}



int main(int argc, char* argv[])
{
  using namespace rapidjson;
  using namespace libtorrent;

  bool quiet = false;
  for (int index = 1; index < argc; ++index)
    if (string(argv[index]) == "--quiet")
      {
	quiet = true;
	for (int next = index + 1; next < argc; ++next)
	  argv[next - 1] = argv[next];
	--argc;
	--index;
      }
  const scoped_quiet_output quiet_output(quiet);

  strings countries;
  string country_boundaries, country_registry, region_file, map_style;
  for (int index = 1; index < argc; ++index)
    {
      const string flag(argv[index]);
      if (flag == "--country" || flag == "--country-boundaries" || flag == "--country-iso-registry" || flag == "--region-definition" || flag == "--map-style")
        {
          if (index + 1 == argc) { std::cerr << "missing value for " << flag << std::endl; return 2; }
          if (flag == "--country") countries.push_back(argv[index+1]);
          else if (flag == "--country-boundaries") country_boundaries = argv[index+1];
          else if (flag == "--country-iso-registry") country_registry = argv[index+1];
          else if (flag == "--region-definition") region_file = argv[index+1];
          else map_style = argv[index+1];
          for (int next=index+2; next<argc; ++next) argv[next-2]=argv[next];
          argc-=2; --index;
        }
    }
  if (!countries.empty() || !region_file.empty())
    {
      if (country_boundaries.empty() || country_registry.empty())
        { std::cerr << "country rendering requires --country-boundaries and --country-iso-registry" << std::endl; return 2; }
      if (argc < 2 || (string(argv[1]) != "--cumulative-maps" && string(argv[1]) != "--cumulative-product-maps"))
        { std::cerr << "--country requires a cumulative map input route" << std::endl; return 2; }
      try {
        countries = country_detail::validate_requests(countries,country_boundaries,country_registry);
        if (!region_file.empty()) {
          const auto definitions=deserialize_json_to_dom_object(region_file);
          if (!definitions.HasMember("regions") || !definitions["regions"].IsArray())throw std::invalid_argument("invalid region definitions");
          for(const auto& r:definitions["regions"].GetArray()) {
            const string id=r["id"].GetString();strings codes;
            if (id.empty() || id.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")!=string::npos ||
                std::find(countries.begin(),countries.end(),id)!=countries.end())throw std::invalid_argument("invalid or duplicate region ID");
            for(const auto& c:r["country_codes"].GetArray())codes.push_back(c.GetString());
            const auto valid=country_detail::validate_requests(codes,country_boundaries,country_registry);
            if(valid.empty() || valid.size()!=codes.size())throw std::invalid_argument("empty or duplicate region membership");
            countries.push_back(id);
          }
        }
      }
      catch (const std::exception& error) { std::cerr << error.what() << std::endl; return 2; }
    }

  // Input file, output directory.
  string input1, input2, input3;
  if (argc > 1)
    input1 = argv[1];
  else
    {
      std::cerr << usage() << std::endl;
      return 1;
    }

  if (argc > 2)
    input2 = argv[2];
  if (argc > 3)
    input3 = argv[3];

  // Time point.
  auto now = time_point_as_string(std::chrono::system_clock::now(), true);

  // Output.
  string odir = io::get_output_directory("tmp");
  io::pre_check_output_directory(odir);
  // One shared media-object audit plate for every cartographic branch:
  // ocean is rgb(242,242,242), land is white.
  const ckproj ck_44x22_audit(f44x22h,
				 "earth-ck-44-22.gray-water242-landwhite");
  const cartography<ckproj> ckwe_audit(f44x22h, ck_44x22_audit, true);
  const auto& carto = ckwe_audit;

  // Cumulative data maps: deserialize the cumulative cache, geolocate
  // the per-BTIH swarm IPs, and render sized carto maps partitioned by
  // resolution (>= 1080p, < 1080p) with per-member colors.
  if (argc > 1 && string(argv[1]) == "--cumulative-maps")
    {
      if (argc < 4)
	{
	  std::cerr << "usage: a60-carto-geo.exe --cumulative-maps "
		    << "CACHE_DIR COLLECTION_KEY" << std::endl;
	  return 1;
	}

      const string cache_dir(argv[2]);
      const string collection_key(argv[3]);
      const collection_factory& factory = collection_catalog();
      auto collection_pointer = factory.get_unique(collection_key);
      if (!collection_pointer)
	{
	  std::cerr << "unknown collection key: " << collection_key
		    << std::endl;
	  return 2;
	}
      collection cll(*collection_pointer);
      cll.initialize_ids_and_members();

      io::set_run_time_resources(cache_dir, cache_dir);

      swarm_geos wcllu = coalesce_with_unique_btiha(cll, "cumulative");
      weigh_unique_collection(wcllu);
      if (countries.empty()) render_cumulative_maps(wcllu, carto, odir);
      else {
        cumulative_map_renderer renderer(wcllu,carto,odir,country_boundaries,countries,"sample-cache-cumulative",region_file,map_style);
        renderer.write_source_accounting();
        for (const string& code : countries) renderer.render_cumulative_maps_by_country(code);
      }
      return 0;
    }

  // Reproduce those maps from an already published cumulative by-BTIH
  // GeoJSON product. This path deliberately has no cache input.
  if (argc > 1 && string(argv[1]) == "--cumulative-product-maps")
    {
      if (argc < 5)
	{
	  std::cerr << "usage: a60-carto-geo.exe "
		    << "--cumulative-product-maps "
		    << "CUMULATIVE-BTIHA-GEOJSON BTIHA-METADATA-JSON "
		    << "COLLECTION_KEY" << std::endl;
	  return 1;
	}
      const string product(argv[2]);
      const string metadata_product(argv[3]);
      const string collection_key(argv[4]);
      const collection_factory& factory = collection_catalog();
      auto collection_pointer = factory.get_unique(collection_key);
      if (!collection_pointer)
	{
	  std::cerr << "unknown collection key: " << collection_key
		    << std::endl;
	  return 2;
	}
      published_btiha_totals totals;
      collection cll = collection_from_btiha_product(
	collection(*collection_pointer), metadata_product, totals);
      swarm_geos wcllu = deserialize_swarm_geos_by_btiha(
	cll, product, totals);
      if (countries.empty()) render_cumulative_maps(wcllu, carto, odir, false);
      else {
        cumulative_map_renderer renderer(wcllu,carto,odir,country_boundaries,countries,"cumulative-geojson",region_file,map_style);
        renderer.write_source_accounting();
        for (const string& code : countries) renderer.render_cumulative_maps_by_country(code);
      }
      return 0;
    }

  // 1
  // pre_check_geoip_install();


  //auto& carto = ckwecarto_engc;
  //auto& carto = ckh4starxcarto_engc;


  // 2
  augment_carto_geo_specific(odir, carto, "geo-specific-points");

  // 3
  //augment_carto_composite(odir, ckcarto);
  //augment_carto_variations(odir, ckcarto);

  // 4 slices
  //augment_carto_slices(odir, ckh2carto_1080p, ckh2state);
  //augment_carto_slices(odir, ckh2carto_engc, ckh2state);

  //augment_carto_slices(odir, ckh4starxcarto_a5, ckh4state);
  //augment_carto_slices(odir, ckh4carto_engc, ckh4state);
  //augment_carto_slices(odir, ckh4starxcarto_engc, ckh4state);

  //augment_carto_slices(odir, ckh4carto_44x22, ckh4state);

  // 5
  augment_swarm_features_geojson(input1, carto, odir);

  return 0;
}
