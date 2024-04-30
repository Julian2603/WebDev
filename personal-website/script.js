// changes the bg of the navbar when scrolling 
window.addEventListener('scroll', function() {
    var navbar = document.getElementById('navbar');
    if (window.scrollY > 0) {
        navbar.classList.add('navbar-solid');
    } else {
        navbar.classList.remove('navbar-solid');
    }
});

//  toggles the visibility of name-section based on screen width
window.addEventListener('resize', function() {
    var nameSection = document.querySelector('.name-section');
    var profileImage = document.getElementById('profile-image');
    if (window.innerWidth <= 768) {
        nameSection.classList.add('hide');
        profileImage.classList.remove('hide');
    } else {
        nameSection.classList.remove('hide');
        profileImage.classList.add('hide');
    }
});
