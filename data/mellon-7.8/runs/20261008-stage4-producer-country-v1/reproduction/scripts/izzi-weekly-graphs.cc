// Reviewed weekly series through Izzi's native line-graph and marker APIs.
#include "izzi-svg.h"
#include "izzi-svg-graphs-line.h"
#include "izzi-svg-fonts.h"
#include <rapidjson/document.h>
#include <fstream>
#include <iomanip>

using std::string;
string number(double x) { std::ostringstream s; s<<std::fixed<<std::setprecision(5)<<x;return s.str(); }
void text(svg::svg_element& out,double x,double y,const string& s,int size=18,const string& anchor="start") {
  out.add_raw("<text x=\""+number(x)+"\" y=\""+number(y)+"\" font-family=\"DejaVu Sans,sans-serif\" font-size=\""+std::to_string(size)+"\" text-anchor=\""+anchor+"\" fill=\"#26313a\">"+svg::escape_xml_attribute(s)+"</text>");
}
svg::color_qi parse_color(const string& value) {
  return svg::color_qi(std::stoi(value.substr(1,2),nullptr,16),std::stoi(value.substr(3,2),nullptr,16),std::stoi(value.substr(5,2),nullptr,16));
}
string label(double v,bool percent) {
  const double scale=percent?1:(v>=1000000?1000000:(v>=1000?1000:1));
  std::ostringstream s;s<<std::setprecision(3)<<v/scale;
  return s.str()+(percent?"%":(scale==1000000?"m":scale==1000?"k":""));
}
double ceiling(double value) {
  if(value<=0)return 1;
  const double base=std::pow(10.,std::floor(std::log10(value)));
  return std::ceil(value/base*2)/2*base;
}
// Generator convention: follow the animation Disney+ subpage.
// https://alpha60-devops.github.io/alpha60-results-animation/docs/disney_plus.html
// Use native Izzi plates and put media-object names ON their lines (12pt
// Atkinson Hyperlegible, right aligned); never add a separate series legend.
// Standard 1920 x 1080 Izzi plates, matching Alpha60 meta-collection graphs.
// The library authors axes, bilateral ticks, grid and titles. Only original
// measurement units are exposed; normalizing draw coordinates avoids the
// pinned library's integer range helper truncating fractional ITU weights.
void render_standard(const rapidjson::Document& doc, const char* destination) {
  using namespace svg;
  const area<> plate{1920,1080};
  svg_element out(destination,area<>{1920.,1080.*doc["panels"].Size()});
  add_atkinson_hyperlegible_font(out);
  out.add_raw("<rect width=\"100%\" height=\"100%\" fill=\"white\"/>");
  const marker_shape forms[]={marker_shape::circle,marker_shape::square,
    marker_shape::triangle,marker_shape::hexagon,marker_shape::x,marker_shape::octahedron,marker_shape::sunburst};
  auto label=[&](const string& value,point_2t position,int size) {
    typography typo=k::hyperl_typo;typo._M_size=size;
    styled_text(out,value,position,typo);
  };
  for(rapidjson::SizeType i=0;i<doc["panels"].Size();++i) {
    const auto& panel=doc["panels"][i];double maximum=0;
    for(const auto& series:panel["series"].GetArray())
      for(const auto& p:series["points"].GetArray()) maximum=std::max(maximum,p["y"].GetDouble());
    const double target=maximum*1.08;
    const double base10=target>0?std::pow(10.,std::floor(std::log10(target))):1;
    for(double multiplier: {1.,2.,5.,10.}) if(target<=base10*multiplier) {
      maximum=base10*multiplier;break;
    }
    if(panel.HasMember("y_max"))maximum=panel["y_max"].GetDouble();
    const bool percent=panel["unit"]=="percent";
    const double unit=percent?1:(maximum>=1000000?1000000:(maximum>=1000?1000:1));
    const string unit_label=percent?"%":(unit==1000000?"M":(unit==1000?"k":""));
    const point_2t xrange{doc["xmin"].GetDouble(),doc["xmax"].GetDouble()};
    const point_2t draw_yrange{0,100000000};
    const style base={color::black,0,color::black,1,2};
    auto visibility=select::title|select::ticks|select::axis|select::vector|select::linex;
    // This Izzi revision's micro grid labels cast to integers. Enable them
    // only when that preserves the tick values (e.g. not half-percent ticks).
    if(std::fmod(maximum/unit,10.)==0)visibility=visibility|select::alt;
    string panel_title=panel["title"].GetString();
    if(string(doc["title"].GetString()).rfind("Weekly country ",0)==0)
      panel_title+=" · "+string(doc["title"].GetString());
    graph_rstate annotations{visibility,
      panel_title,plate,chart_line_style_1,
      doc["xlabel"].GetString(),panel["ylabel"].GetString(),"",unit_label,
      base,{"",marker_shape::none,0,"","","round",""},{0,0},"",""};
    vrange ticks;
    for(const auto& tick:doc["ticks"].GetArray())ticks.push_back({tick[0].GetDouble(),0});
    out.add_raw("<g data-izzi-layout=\"standard\" transform=\"translate(0 "+std::to_string(i*1080)+")\">");
    out.add_element(make_line_graph_annotations(ticks,annotations,xrange,{0,maximum/unit},1,1,k::hyperl_typo));
    label(doc["subtitle"].GetString(),{960,163},19);
    std::vector<std::array<double,4>> label_boxes;
    for(rapidjson::SizeType j=0;j<panel["series"].Size();++j) {
      const auto& series=panel["series"][j];
      const style stroke={parse_color(series["color"].GetString()),0,parse_color(series["color"].GetString()),1,2.5};
      graph_rstate state{select::vector,"panel-"+std::to_string(i)+"-series-"+std::to_string(j),
        plate,chart_line_style_1,doc["xlabel"].GetString(),panel["ylabel"].GetString(),"","",stroke,
        {"",marker_shape::none,0,series["dash"].GetString(),"","round",""},{0,0},"",""};
      vrange points;
      for(const auto& p:series["points"].GetArray())points.push_back({p["x"].GetDouble(),p["y"].GetDouble()/maximum*100000000});
      if(points.empty())throw std::runtime_error("empty worldwide series");
      out.add_raw("<g class=\"izzi-line-series\" tabindex=\"0\" role=\"group\" aria-label=\""+
        escape_xml_attribute(series["name"].GetString())+"\" data-series=\""+
        escape_xml_attribute(series["name"].GetString())+"\" data-collection-key=\""+
        escape_xml_attribute(series.HasMember("collection_key")?series["collection_key"].GetString():series["name"].GetString())+"\">");
      vrange segment;
      auto flush=[&](){if(!segment.empty()){out.add_element(make_line_graph(segment,state,xrange,draw_yrange));segment.clear();}};
      for(const auto& p:points) {
        if(!segment.empty()) {
          const auto gap=std::get<0>(p)-std::get<0>(segment.back());
          if(gap<=0)throw std::runtime_error("unordered weekly points");
          if(gap>1.001)flush();
        }
        segment.push_back(p);
      }
      flush();
      const auto positions=transform_to_graph_points(points,state,xrange,draw_yrange);
      style marker=stroke;marker._M_fill_opacity=1;
      for(std::size_t n=0;n<points.size();++n)
        out.add_raw(make_marker_instance(forms[j%7],positions[n],marker,6,series["points"][n]["tooltip"].GetString()));
      // Match graph_by in a60-meta-collection-graph-json.h: the media-object
      // name is right-aligned just above its line, using native 12pt type.
      // When ending values coincide, anchor at an earlier observed point on
      // that same line rather than letting the labels cover one another.
      const string name=series.HasMember("line_label")?series["line_label"].GetString():series["name"].GetString();
      typography typo=k::hyperl_typo;
      typo._M_align=typography::align::right;
      typo._M_anchor=typography::anchor::end;
      typo._M_size=graph_rstate::tpsz;
      const double label_width=name.size()*graph_rstate::tpsz*.8;
      std::size_t index=positions.size()-1;
      std::array<double,4> box{};
      bool placed=false;
      double label_x=0, label_y=0;
      for(std::size_t candidate=positions.size();candidate-->0;) {
        const auto [x,y]=positions[candidate];
        const double baseline=y-graph_rstate::tticsz/2.;
        box={x-label_width,baseline-16,x,baseline+4};
        if(box[0]<graph_rstate::xmargin || box[1]<graph_rstate::ymargin)continue;
        bool collision=false;
        for(const auto& used:label_boxes)
          if(box[0]<used[2]+5 && box[2]>used[0]-5 && box[1]<used[3]+5 && box[3]>used[1]-5)collision=true;
        if(!collision){index=candidate;placed=true;label_x=x;label_y=baseline;break;}
      }
      // Larger collections can have coincident or very short lines. An opt-in
      // leader keeps each label attached to an observed point without overlap.
      bool callout=false;
      if(!placed && doc.HasMember("allow_label_callouts") && doc["allow_label_callouts"].GetBool()) {
        for(int offset=0;offset<=600 && !placed;offset+=24) {
          for(const int sign: {-1,1}) {
            const auto [x,y]=positions.back();
            const double tx=std::max(x,graph_rstate::xmargin+label_width+8.);
            const double ty=y-graph_rstate::tticsz/2.+sign*offset;
            box={tx-label_width,ty-16,tx,ty+4};
            if(box[0]<graph_rstate::xmargin || box[2]>1920-graph_rstate::xmargin
               || box[1]<graph_rstate::ymargin || box[3]>1080-graph_rstate::ymargin)continue;
            bool collision=false;
            for(const auto& used:label_boxes)
              if(box[0]<used[2]+5 && box[2]>used[0]-5 && box[1]<used[3]+5 && box[3]>used[1]-5)collision=true;
            if(!collision){index=positions.size()-1;placed=true;callout=true;label_x=tx;label_y=ty;break;}
          }
        }
      }
      if(!placed)throw std::runtime_error("no clear line-label position for "+name);
      label_boxes.push_back(box);
      const auto [mx,my]=positions[index];
      out.add_raw("<g class=\"series-label\" data-label-week=\""+number(series["points"][index]["x"].GetDouble())+"\">");
      if(callout)
        out.add_raw("<line class=\"label-leader\" x1=\""+number(mx)+"\" y1=\""+number(my)
          +"\" x2=\""+number(label_x)+"\" y2=\""+number(label_y+4)
          +"\" stroke=\""+series["color"].GetString()+"\" stroke-width=\"1\"/>");
      out.add_element(style_text(name,{label_x,label_y},typo));
      out.add_raw("</g>");
      out.add_raw("</g>");
    }
    const string count=panel["series"].Size()==6?"six":(panel["series"].Size()==7?"seven":std::to_string(panel["series"].Size()));
    const string footer=doc.HasMember("footer")?doc["footer"].GetString():
      "All "+count+" media objects · weekly geographic interval "+
      (percent?"shares · percent of the worldwide role total":"weights · provisional 2026 ITU reference");
    label(footer,{960,1052},17);
    out.add_raw("</g>");
  }
}
int main(int argc,char** argv) {
  if(argc!=3)return 2;
  std::ifstream input(argv[1]);string raw((std::istreambuf_iterator<char>(input)),{});
  rapidjson::Document doc;doc.Parse(raw.c_str());if(doc.HasParseError())throw std::runtime_error("invalid chart JSON");
  if(!doc.HasMember("layout") || doc["layout"]=="izzi-standard") {
    render_standard(doc,argv[2]);return 0;
  }
  using namespace svg;
  const int columns=doc["columns"].GetInt(),rows=(doc["panels"].Size()+columns-1)/columns;
  const double width=1200,cell=width/columns,plot_width=cell-125,plot_height=columns==1?255:270;
  const auto& legend=doc["panels"][0]["series"];
  const int legend_cols=legend.Size()>4?3:2,legend_rows=(legend.Size()+legend_cols-1)/legend_cols;
  const double header=100+legend_rows*28,panel_height=plot_height+130,height=header+rows*panel_height+25;
  svg_element out(argv[2],area<>{width,height});
  out.add_raw("<rect width=\"100%\" height=\"100%\" fill=\"white\"/>");
  text(out,25,32,doc["title"].GetString(),25);text(out,25,62,doc["subtitle"].GetString(),17);
  const marker_shape forms[]={marker_shape::circle,marker_shape::square,marker_shape::triangle,marker_shape::hexagon,marker_shape::x,marker_shape::octahedron,marker_shape::sunburst};
  for(rapidjson::SizeType j=0;j<legend.Size();++j) {
    const auto& s=legend[j];const double x=30+(j%legend_cols)*(width/legend_cols),y=96+(j/legend_cols)*28;
    style sty={parse_color(s["color"].GetString()),1,parse_color(s["color"].GetString()),1,2};
    stroke_style stroke={"",forms[j%7],0,s["dash"].GetString(),"","round",""};
    out.add_element(make_polyline({{x,y-5},{x+42,y-5}},sty,stroke));
    out.add_raw(make_marker_instance(forms[j%7],{x+21,y-5},sty,4));
    text(out,x+54,y,s["name"].GetString(),18);
  }
  for(rapidjson::SizeType i=0;i<doc["panels"].Size();++i) {
    const auto& panel=doc["panels"][i];const double x=(i%columns)*cell+88,y=header+(i/columns)*panel_height+50;
    double maximum=0;
    for(const auto& series:panel["series"].GetArray())for(const auto& p:series["points"].GetArray())maximum=std::max(maximum,p["y"].GetDouble());
    maximum=panel.HasMember("y_max")?panel["y_max"].GetDouble():ceiling(maximum*1.08);
    if(maximum<=0)throw std::runtime_error("invalid y domain");
    // This Izzi revision's range helper takes int coordinates. Normalize only
    // rendering Y values to a safe 1e8 domain so fractional shares and scaled
    // weights survive the helper without truncating to whole percentage points.
    // Original measurements remain in JSON, axes and marker tooltips.
    const point_2t xrange={doc["xmin"].GetDouble(),doc["xmax"].GetDouble()},yrange={0,100000000};
    text(out,x,y-25,panel["title"].GetString(),21);
    const bool percent=panel["unit"]=="percent";
    const style axis={svg::color::none,0,svg::color::black,1,1};
    const style grid={svg::color::none,0,svg::color::gray10,1,0.6};
    out.add_element(make_line({x,y},{x,y+plot_height},axis));out.add_element(make_line({x,y+plot_height},{x+plot_width,y+plot_height},axis));
    for(int tick=0;tick<=5;++tick) {
      const double value=maximum*tick/5,yy=y+plot_height-plot_height*tick/5;
      if(tick)out.add_element(make_line({x,yy},{x+plot_width,yy},grid));
      text(out,x-10,yy+5,label(value,percent),16,"end");
    }
    for(const auto& tick:doc["ticks"].GetArray()) {
      const double xx=x+plot_width*(tick[0].GetDouble()-std::get<0>(xrange))/(std::get<1>(xrange)-std::get<0>(xrange));
      out.add_element(make_line({xx,y+plot_height},{xx,y+plot_height+5},axis));text(out,xx,y+plot_height+27,tick[1].GetString(),16,"middle");
    }
    text(out,x+plot_width/2,y+plot_height+57,doc["xlabel"].GetString(),17,"middle");
    out.add_raw("<g transform=\"translate("+number(x-67)+" "+number(y+plot_height/2)+") rotate(-90)\">");
    text(out,0,0,panel["ylabel"].GetString(),17,"middle");out.add_raw("</g>");
    for(rapidjson::SizeType j=0;j<panel["series"].Size();++j) {
      const auto& s=panel["series"][j];const string id="panel-"+std::to_string(i)+"-series-"+std::to_string(j);
      style sty={parse_color(s["color"].GetString()),1,parse_color(s["color"].GetString()),1,2};
      style line_style=sty;line_style._M_fill_opacity=0;
      graph_rstate state{select::vector,id,{plot_width+400,plot_height+400},chart_line_style_1,"Weeks",panel["ylabel"].GetString(),"","",sty,
                         {"",marker_shape::none,0,s["dash"].GetString(),"","round",""},{0,0},"",""};
      state.lstyle=line_style;
      vrange points;
      for(const auto& p:s["points"].GetArray())points.push_back({p["x"].GetDouble(),p["y"].GetDouble()/maximum*100000000});
      if(points.empty())continue;
      for(std::size_t n=1;n<points.size();++n)if(std::get<0>(points[n])<=std::get<0>(points[n-1]))throw std::runtime_error("unordered weekly points");
      out.add_raw("<g data-series=\""+escape_xml_attribute(s["name"].GetString())+"\" transform=\"translate("+number(x-200)+" "+number(y-200)+")\">");
      // Split at missing intervals so an interior gap never gets interpolated.
      vrange segment;
      auto flush=[&](){if(!segment.empty()){out.add_element(make_line_graph(segment,state,xrange,yrange,4));segment.clear();}};
      for(const auto& p:points){if(!segment.empty()&&std::get<0>(p)-std::get<0>(segment.back())>1.001)flush();segment.push_back(p);}flush();
      const auto positions=transform_to_graph_points(points,state,xrange,yrange);
      for(std::size_t n=0;n<points.size();++n)out.add_raw(make_marker_instance(forms[j%7],positions[n],sty,4,s["points"][n]["tooltip"].GetString()));
      out.add_raw("</g>");
    }
  }
  text(out,25,height-10,"Izzi native weekly line graphs · missing intervals are unplotted · exact values in the accompanying ledger",15);
}
