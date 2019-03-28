// Allowing a smoother transition for navigating around the site
function smoothScroll(target, duration){
  var target = document.querySelector(target);
  var targetPosition = target.getBoundingClientRect().top;
  var startPosition = window.pageYOffset;
  var distance = targetPosition - startPosition;
  var startTime = null;

  function animationScroll(currentTime){
    if(startTime === null) startTime = currentTime;
    var timeElapsed = currentTime - startTime;
    var runAnimation = ease(timeElapsed, startPosition, distance, duration);
    window.scrollTo(0, runAnimation);
    if(timeElapsed < duration) requestAnimationFrame(animationScroll);
  }
  function ease(t, b, c, d) {
	return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b;
}
  requestAnimationFrame(animationScroll);
}


// tying the bottom left and right buttons for ease of scrolling
// left for the lefthanded
var bottomOfPage_left = document.querySelector('.bottomOfPage_left');
var bottomOfPage_right = document.querySelector('.bottomOfPage_right');

bottomOfPage_right.addEventListener('click', function(){
  smoothScroll('.topOfPage', 1500);
})

bottomOfPage_left.addEventListener('click', function(){
  smoothScroll('.topOfPage', 1500);
})
