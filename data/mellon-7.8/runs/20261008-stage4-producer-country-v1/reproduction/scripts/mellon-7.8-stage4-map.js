/* Pinned local Leaflet; no external map tiles, tracking or geolocation calls. */
(async()=>{
'use strict';
const pointer=await (await fetch('../data/mellon-7.8-stage4-current.json')).json();
const base='../data/mellon-7.8/runs/'+pointer.run_id+'/';
const map=L.map('map',{preferCanvas:true,worldCopyJump:false,minZoom:0,maxZoom:10}).fitBounds([[-60,-180],[85,180]]);
const renderer=L.canvas({padding:.3});
const outline=await (await fetch('stage4-vendor/world.geojson')).json();
L.geoJSON(outline,{interactive:false,style:{color:'#888',weight:.5,fillColor:'#fff',fillOpacity:1},renderer}).addTo(map);
let layer=null,geo=null;const cache=new Map();let request=0;
const el=id=>document.getElementById(id);
function field(){return el('role').value+'_'+el('mode').value+'_delta_pp';}
function color(v,scale){const q=Math.min(1,Math.abs(v)/scale),rgb=v>=0?[23,91,140]:[161,72,26];return 'rgb('+rgb.map(x=>Math.round(245+(x-245)*q)).join(',')+')';}
function paint(){
 if(!geo)return;if(layer)map.removeLayer(layer);const f=field(),mask=el('view').value==='coverage';
 el('detail').textContent='';
 const eligible=geo.features.filter(x=>x.properties[f]!==null);
 const magnitudes=eligible.map(x=>Math.abs(x.properties[f])).sort((a,b)=>a-b);
 const scale=magnitudes[Math.floor((magnitudes.length-1)*.95)]||.001;
 const show=mask?geo.features:eligible;
 layer=L.geoJSON({type:'FeatureCollection',features:show},{renderer,style:x=>({color:mask?(x.properties.full_window_comparable?'#175b8c':'#777'):color(x.properties[f],scale),weight:.5,fillColor:mask?(x.properties.full_window_comparable?'#175b8c':'#999'):color(x.properties[f],scale),fillOpacity:.8}),onEachFeature:(x,l)=>l.on('click',()=>{const p=x.properties;el('detail').textContent=p.h3+' · '+p.countries.join(', ')+' · '+(p[f]===null?'Not comparable over the full window':p[f].toFixed(5)+' percentage points')+' · '+p.common_intervals+'/'+p.expected_intervals+' common intervals';})}).addTo(map);
 const m=geo.metadata;el('title').textContent=el('dataset').selectedOptions[0].textContent+' — H3 resolution 5';
 el('status').textContent=m.full_comparable_cells.toLocaleString()+' fully comparable cells out of '+m.union_cells.toLocaleString()+' observed on either side; '+m.weeks.length+' aligned sampling weeks. Missing cells remain unavailable.';
 el('legend').innerHTML=mask?'<span class="swatch" style="background:#175b8c"></span>Full common coverage · <span class="swatch" style="background:#999"></span>Incomplete coverage':'<span class="swatch" style="background:#a1481a"></span>Second work larger · <span class="swatch" style="background:#175b8c"></span>First work larger · Color saturates at ±'+scale.toFixed(5)+' percentage points (95th percentile); exact values remain in the table and download.';
 const tbody=el('cells');tbody.replaceChildren();
 eligible.sort((a,b)=>Math.abs(b.properties[f])-Math.abs(a.properties[f])).slice(0,20).forEach(x=>{const tr=document.createElement('tr'),td=document.createElement('td'),button=document.createElement('button');button.textContent=x.properties.h3;button.addEventListener('click',()=>{map.fitBounds(L.geoJSON(x).getBounds(),{maxZoom:7});el('detail').textContent=x.properties.h3+' · '+x.properties[f].toFixed(5)+' percentage points';});td.append(button);tr.append(td);for(const text of [x.properties.countries.join(', '),x.properties[f].toFixed(5)]){const c=document.createElement('td');c.textContent=text;tr.append(c);}tbody.append(tr);});
 document.body.dataset.ready='true';
}
async function load(){const token=++request;document.body.dataset.ready='false';const name=el('dataset').value;if(!cache.has(name)){const r=await fetch(base+name+'.geojson');if(!r.ok)throw Error('Map download failed: '+r.status);cache.set(name,await r.json());}if(token!==request)return;geo=cache.get(name);el('download').href=base+name+'.geojson';paint();}
el('dataset').addEventListener('change',()=>load().catch(error=>{el('status').textContent=error.message;}));
for(const id of ['role','mode','view'])el(id).addEventListener('change',paint);
el('region').addEventListener('change',()=>{const views={world:[[-60,-180],[85,180]],asia:[[-12,65],[55,145]],europe:[[33,-14],[71,37]],'north-america':[[15,-165],[75,-48]]};map.fitBounds(views[el('region').value]);});
await load();
})().catch(error=>{document.getElementById('status').textContent='Unable to load map: '+error.message;});
