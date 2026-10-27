// Pulls the prompt data out of board.html into prompts.md.
// node merch/extract-prompts.js merch/board.html merch/prompts.md
const fs=require('fs');
const s=fs.readFileSync(process.argv[2],'utf8');
const js=s.match(/<script>([\s\S]*)<\/script>/)[1];
const base=js.match(/var BASE=(.*?);\n/)[1];
const neg=js.match(/var NEG=(.*?);\n/)[1];
const concepts=js.slice(js.indexOf('var concepts=')+'var concepts='.length, js.indexOf('\n  var root='));
const pack=js.slice(js.indexOf('var packData=')+'var packData='.length, js.indexOf('\n  var packRoot='));
const tracks=js.slice(js.indexOf('var tracks = ')+'var tracks = '.length, js.indexOf('\n  var roman'));
const BASE=eval(base), NEG=eval(neg);
const C=eval('('+concepts.replace(/;\s*$/,'')+')');
const P=eval('('+pack.replace(/;\s*$/,'')+')');
const T=eval('('+tracks.replace(/;\s*$/,'')+')');
const roman=["I","II","III","IV","V","VI","VII","VIII"];
let out='# Grok Imagine prompts\n\nSettings: Quality mode. Art-only 3:4, flat lay 16:9, on-body 4:5, macro 1:1. Four generations per prompt, keep one. Inspect every character. Tracklist, token legend and sleeve text never render: generate art without them and typeset in Figma.\n\nFix a render (upload and edit): `Change the text to read exactly "SÓLHVARF". Keep the lettering style, placement, colours and everything else identical.`\n\nReject any render with a skull, pentagram, inverted cross, sun wheel, horned helmet or recognisable band logo. Prompt again, do not retouch.\n\n## Tracklist\n\n';
for(const l of ['no','sv','en']){out+='### '+{no:'Norsk',sv:'Svenska',en:'English'}[l]+'\n\n';T[l].forEach((t,i)=>{out+=roman[i]+'. '+t[0]+(t[1]?' ('+t[1]+')':'')+'\n'});out+='\n';}
for(const c of C){
  const d=P[c.id];
  const garment = c.id==='jol' ? 'oversized heavyweight unbleached ecru cotton t-shirt' : (c.id==='turne' ? 'heavyweight black longsleeve t-shirt with vintage acid wash' : (c.id==='endrborinn' ? 'standard flat black t-shirt' : 'oversized heavyweight black t-shirt with vintage acid wash'));
  out+='## '+c.name+' · '+c.tag+'\n\n'+c.thesis+'\n\n';
  out+='### Flat lay · 16:9\n\n```\n'+c.prompt+'\n```\n\n';
  out+='### Art only · 3:4\n\n```\nIsolated t-shirt print artwork on a flat pure black background, no garment, no mockup, centred. Subject: '+d.art+'. Ink: '+d.ink+'. Style: '+d.style+'. '+NEG+'\n```\n\n';
  out+='### On body · 4:5\n\n```\nEditorial photograph: '+d.scene+'. The '+garment+' carries a screen print: '+d.art+'. Ink: '+d.ink+'. Natural light, shallow depth of field, 35 mm film grain, muted cold palette. '+NEG+'\n```\n\n';
  out+='### Detail · 1:1\n\n```\nExtreme close-up macro photograph of a screen print on a '+garment+': '+d.macro+'. Ink: '+d.ink+'. Shallow depth of field, soft side light, realistic fabric texture. '+NEG+'\n```\n\n';
}
fs.writeFileSync(process.argv[3],out);
console.log('prompts written', out.length);
