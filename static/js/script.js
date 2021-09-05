// external js: flickity.pkgd.js

var flkty = new Flickity('.carousel');

var buttonGroup = document.querySelector('.button-group');

buttonGroup.addEventListener( 'click', function( event ) {
  // filter for button clicks
  if ( !matchesSelector( event.target, '.button' ) ) {
    return;
  }
  let group = event.target.dataset.group;
  flkty.selectCell(`[data-group="${group}"]`);
});

let selectedNavButton = buttonGroup.querySelector('.is-selected');

flkty.on( 'change', function() {
  let group = flkty.selectedElement.dataset.group;
  let navButton = buttonGroup.querySelector(`[data-group="${group}"]`);
  if ( navButton != selectedNavButton ) {
    selectedNavButton.classList.remove('is-selected');
    navButton.classList.add('is-selected');
    selectedNavButton = navButton;
  }
})