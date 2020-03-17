$('#hide-control').click(function () {
    $('.title').fadeOut(250, 'linear')
    $('.menu-bar').animate({
        opacity: 1,
        top: 0,
    }, 800)
})