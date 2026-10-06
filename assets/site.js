// ролики: играют, только когда видны; при «меньше движения» — с кнопками
(function(){
  var vs=[].slice.call(document.querySelectorAll("video:not([data-manual])"));
  if(!vs.length)return;
  var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
  vs.forEach(function(v){v.removeAttribute("autoplay");v.muted=true;if(reduce)v.controls=true;});
  if(reduce||!("IntersectionObserver" in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    var v=e.target;if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){v.controls=true;});}else v.pause();
  });},{threshold:.25});
  vs.forEach(function(v){io.observe(v);});
})();
