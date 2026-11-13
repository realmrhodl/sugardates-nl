/* SugarDates v8 signup (copied from v5, v8 images/styles) – front-end only.
   Nothing is sent to a server. Role, basics and email may be kept in localStorage as a waitlist placeholder.
   No password is collected. */
(function(){
  var T = window.SD || {};
  var KEY = T.storage || "sugardates-v8";
  var YEAR_MAX = new Date().getFullYear() - (T.minAge || 18), YEAR_MIN = YEAR_MAX - 70;
  var STEPS = ["role","about","account"];
  var IMG = {baby:"baby", daddy:"daddy"};
  var state = {role:"",displayName:"",location:"",birthYear:"",who:"",what:[],bio:"",email:"",done:false};
  var i = 0;
  var panel = document.getElementById("panel"), back = document.getElementById("back-btn"),
      count = document.getElementById("step-count"), fill = document.getElementById("progress-fill"),
      live = document.getElementById("step-live"), trust = document.getElementById("trust");
  var TICK = '<span class="tick" aria-hidden="true"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.5"><path d="M5 12.5l5 5 9-10"/></svg></span>';
  var ARR = '';

  function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];}); }
  function fmt(s,o){ return s.replace(/\{(\w+)\}/g,function(_,k){ return o[k]; }); }
  function label(list,id){ for(var k=0;k<list.length;k++) if(list[k][0]===id) return list[k][1]; return id; }
  function save(){ try{ var c=JSON.parse(JSON.stringify(state)); c.i=i; localStorage.setItem(KEY,JSON.stringify(c)); }catch(e){} }
  function load(){ try{ var d=JSON.parse(localStorage.getItem(KEY)||"null"); if(!d) return;
      ["role","displayName","location","birthYear","who","bio","email"].forEach(function(k){ if(typeof d[k]==="string") state[k]=d[k]; });
      if(Array.isArray(d.what)) state.what=d.what.filter(function(x){return typeof x==="string";});
      state.done=!!d.done; if(typeof d.i==="number"&&d.i>=0&&d.i<STEPS.length) i=d.i; }catch(e){} }
  function rm(){ return window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches; }
  function nextBtn(extra){ return '<div class="actions sticky"><button type="button" class="btn btn-primary btn-block" data-next>'+T.next+ARR+'</button>'+(extra||"")+'</div>'; }
  function lead(){ return state.role ? '<p class="personal">'+esc(state.role==="baby"?T.lead_baby:T.lead_daddy)+'</p>' : ""; }
  function opts(list, sel, cls){ return '<div class="opts '+(cls||"")+'" role="group">'+list.map(function(o){ var on=sel.indexOf(o[0])>=0; return '<button type="button" class="opt'+(on?" is-on":"")+'" data-opt="'+o[0]+'" aria-pressed="'+on+'"><span>'+esc(o[1])+'</span>'+TICK+'</button>'; }).join("")+'</div>'; }
  function options(vals, cur){ return vals.map(function(v){ return '<option value="'+esc(v)+'"'+(cur===v?" selected":"")+'>'+esc(v)+'</option>'; }).join(""); }
  function pic(n){ return '<picture><source srcset="'+T.img+n+'-480.webp 480w, '+T.img+n+'-720.webp 720w" sizes="(min-width:960px) 240px, 45vw" type="image/webp"><img src="'+T.img+n+'.jpg" alt="" width="1080" height="1350"></picture>'; }

  function step(id){
    if(id==="role") return '<h1 class="title">'+T.role_h+'</h1><p class="lead2">'+T.role_p+'</p><div class="role-pick">'+
      ["baby","daddy"].map(function(r){ return '<button type="button" class="role-card'+(state.role===r?" is-on":"")+'" data-role="'+r+'">'+pic(IMG[r])+'<span class="rc"><span class="t">'+T["role_"+r+"_t"]+'</span><span class="k">'+T["role_"+r+"_k"]+'</span></span></button>'; }).join("")+'</div><p class="err" id="err" hidden></p>';
    if(id==="about"){
      var years=[]; for(var y=YEAR_MAX;y>=YEAR_MIN;y--) years.push(String(y));
      var loc = T.regions.length
        ? '<optgroup label="'+esc(T.grp_cities)+'">'+options(T.cities,state.location)+'</optgroup><optgroup label="'+esc(T.grp_regions)+'">'+options(T.regions,state.location)+'</optgroup>'
        : options(T.cities,state.location);
      return lead()+'<h1 class="title">'+T.about_h+'</h1><p class="lead2">'+T.about_p+'</p>'+
        '<div class="field"><label for="displayName">'+T.f_name+'</label><input id="displayName" class="inp" type="text" maxlength="32" autocomplete="nickname" value="'+esc(state.displayName)+'"></div>'+
        '<div class="field"><label for="location">'+T.f_loc+'</label><select id="location" class="inp"><option value="">'+esc(T.f_loc_ph)+'</option>'+loc+'<option value="'+esc(T.other)+'"'+(state.location===T.other?" selected":"")+'>'+esc(T.other)+'</option></select></div>'+
        '<div class="field"><label for="birthYear">'+T.f_year+'</label><select id="birthYear" class="inp"><option value="">'+esc(T.f_year_ph)+'</option>'+options(years,state.birthYear)+'</select></div>'+
        '<p class="micro">'+T.about_micro+'</p><p class="err" id="err" hidden></p>'+nextBtn();
    }
    if(id==="looking") return lead()+'<h1 class="title">'+T.looking_h+'</h1><p class="lead2">'+T.looking_p+'</p>'+
      '<p class="grp-label">'+T.grp_who+'</p>'+opts(T.who, state.who?[state.who]:[], "two")+
      '<p class="grp-label">'+T.grp_what+'</p>'+opts(T.what, state.what)+'<p class="err" id="err" hidden></p>'+nextBtn();
    if(id==="bio") return lead()+'<h1 class="title">'+T.bio_h+'</h1><p class="lead2">'+T.bio_p+'</p>'+
      '<div class="field"><label for="bio">'+T.f_bio+'</label><textarea id="bio" class="inp" rows="3" maxlength="120">'+esc(state.bio)+'</textarea></div>'+
      '<p class="micro">'+T.bio_micro+'</p><p class="err" id="err" hidden></p>'+nextBtn('<button type="button" class="btn btn-outline btn-block" data-skip>'+T.skip+'</button>');
    if(id==="account") return lead()+'<h1 class="title">'+T.acc_h+'</h1><p class="lead2">'+T.acc_p+'</p><form id="acc" novalidate>'+
      '<div class="field"><label for="email">'+T.f_email+'</label><input id="email" class="inp" type="email" autocomplete="email" inputmode="email" value="'+esc(state.email)+'"></div>'+
      '<p class="micro">'+T.acc_micro+'</p>'+
      '<label class="chk-row"><input id="age" type="checkbox" class="chk"><span>'+T.chk_age+'</span></label>'+
      '<label class="chk-row"><input id="terms" type="checkbox" class="chk"><span>'+T.chk_terms+'</span></label>'+
      '<p class="err" id="err" hidden></p><div class="actions sticky"><button type="submit" class="btn btn-primary btn-block">'+T.submit+ARR+'</button></div></form>';
    return "";
  }
  function success(){
    var rows=[[T.s_role, state.role==="baby"?T.r_baby:T.r_daddy],[T.s_name,state.displayName],[T.s_loc,state.location],[T.s_year,state.birthYear],[T.s_email,state.email]];
    return '<svg class="ok" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="26" fill="#f3f3f3"/><path d="M16 27l7 7 13-15" fill="none" stroke="#b3122e" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'+
      '<h1 class="title">'+fmt(T.ok_h,{name:esc(state.displayName)})+'</h1><p class="lead2">'+fmt(esc(T.ok_p),{email:esc(state.email)})+'</p>'+
      '<dl class="summary">'+rows.filter(function(r){return r[1];}).map(function(r){return '<div><dt>'+esc(r[0])+'</dt><dd>'+esc(r[1])+'</dd></div>';}).join("")+'</dl>'+
      '<p class="micro">'+T.ok_next+'</p><div class="actions"><a class="btn btn-primary btn-block" href="../">'+T.home+'</a><button type="button" class="btn btn-outline btn-block" id="reset">'+T.reset+'</button></div>';
  }
  function chrome(){
    var t=STEPS.length, n=state.done?t:i+1;
    fill.style.width=Math.round(n/t*100)+"%";
    back.hidden = state.done || i===0;
    count.innerHTML = state.done ? esc(T.done) : (i===t-1 ? "<b>"+esc(T.left1)+"</b> · "+esc(T.steps[STEPS[i]]) : fmt(esc(T.stepOf),{n:"<b>"+n+"</b>",t:t})+' · '+esc(T.steps[STEPS[i]]));
    trust.hidden = state.done;
  }
  var first=true;
  function render(){
    chrome();
    var h = state.done ? success() : step(STEPS[i]);
    function paint(){
      panel.innerHTML=h; panel.classList.remove("is-leave"); bind();
      var hd=panel.querySelector("h1"); if(hd){ hd.setAttribute("tabindex","-1"); if(!first0){ try{hd.focus({preventScroll:true});}catch(e){} } live.textContent=hd.textContent; }
      if(!first0 && window.innerWidth<960){ var m=document.querySelector(".step-meta").getBoundingClientRect().top+scrollY-16; if(scrollY>m||scrollY<m-200) scrollTo({top:m,behavior:rm()?"auto":"smooth"}); }
    }
    var first0=first; first=false;
    if(first0||rm()) return paint();
    panel.classList.add("is-leave"); setTimeout(paint,150);
  }
  function err(msg,el){ var e=document.getElementById("err"); if(e){ e.hidden=false; e.textContent=msg; } if(el){ el.setAttribute("aria-invalid","true"); el.focus(); } }
  function go(d){ var n=i+d; if(n<0||n>=STEPS.length) return; i=n; save(); render(); }
  function val(id){ var el=document.getElementById(id); return el?el.value:""; }
  function bind(){
    var id=state.done?"ok":STEPS[i];
    panel.querySelectorAll("[data-role]").forEach(function(b){ b.addEventListener("click",function(){ state.role=b.getAttribute("data-role"); panel.querySelectorAll("[data-role]").forEach(function(x){x.classList.toggle("is-on",x===b);}); save(); setTimeout(function(){go(1);},rm()?0:200); }); });
    panel.querySelectorAll("[data-opt]").forEach(function(b){ b.addEventListener("click",function(){
      var v=b.getAttribute("data-opt"), group=b.parentNode, single=group.classList.contains("two");
      if(single){ state.who = state.who===v?"":v; group.querySelectorAll(".opt").forEach(function(x){ var on=x.getAttribute("data-opt")===state.who; x.classList.toggle("is-on",on); x.setAttribute("aria-pressed",on); }); }
      else { var k=state.what.indexOf(v); if(k>=0) state.what.splice(k,1); else state.what.push(v); var on=state.what.indexOf(v)>=0; b.classList.toggle("is-on",on); b.setAttribute("aria-pressed",on); }
      save(); var e=document.getElementById("err"); if(e) e.hidden=true; }); });
    var nb=panel.querySelector("[data-next]"); if(nb) nb.addEventListener("click",next);
    var sk=panel.querySelector("[data-skip]"); if(sk) sk.addEventListener("click",function(){ state.bio=""; go(1); });
    var f=document.getElementById("acc"); if(f) f.addEventListener("submit",submit);
    var r=document.getElementById("reset"); if(r) r.addEventListener("click",function(){ try{localStorage.removeItem(KEY);}catch(e){} state={role:"",displayName:"",location:"",birthYear:"",who:"",what:[],bio:"",email:"",done:false}; i=0; render(); });
    ["displayName","location","birthYear"].forEach(function(k){ var el=document.getElementById(k); if(el) el.addEventListener("change",function(){ state[k]=el.value; save(); }); });
  }
  function next(){
    var id=STEPS[i];
    if(id==="about"){
      state.displayName=val("displayName").trim(); state.location=val("location"); state.birthYear=val("birthYear");
      if(!state.displayName) return err(T.e_name,document.getElementById("displayName"));
      if(!state.location) return err(T.e_loc,document.getElementById("location"));
      var y=parseInt(state.birthYear,10); if(!y||y>YEAR_MAX||y<YEAR_MIN) return err(T.e_year,document.getElementById("birthYear"));
    }
    if(id==="looking"){ if(!state.who) return err(T.e_who); if(!state.what.length) return err(T.e_what); }
    if(id==="bio") state.bio=val("bio").trim();
    go(1);
  }
  function submit(ev){
    ev.preventDefault();
    var em=document.getElementById("email");
    var email=em.value.trim();
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return err(T.e_email,em);
    if(!document.getElementById("age").checked) return err(T.e_age,document.getElementById("age"));
    if(!document.getElementById("terms").checked) return err(T.e_terms,document.getElementById("terms"));
    state.email=email; state.done=true; save(); render();
  }
  back.addEventListener("click",function(){ go(-1); });
  load();
  var q=(location.search.match(/[?&]rol=(baby|daddy)/)||[])[1];
  if(q && !state.done){ if(state.role!==q){ state.role=q; } if(i===0) i=1; }
  if(!state.role && !state.done) i=0;
  render();
})();
