(function($) {

  "use strict";

  // Preloader
  var initPreloader = function() {
    $(document).ready(function($) {
      var Body = $('body');
      Body.addClass('preloader-site');
    });
    $(window).load(function() {
      $('.preloader-wrapper').fadeOut();
      $('body').removeClass('preloader-site');
    });
  }

  // Chocolat light box
  var initChocolat = function() {
    Chocolat(document.querySelectorAll('.image-link'), {
      imageSize: 'contain',
      loop: true,
    });
  }

  // Swiper
  var initSwiper = function() {
    var swiper = new Swiper(".main-swiper", {
      speed: 500,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    var category_swiper = new Swiper(".category-carousel", {
      slidesPerView: 6,
      spaceBetween: 30,
      speed: 500,
      navigation: {
        nextEl: ".category-carousel-next",
        prevEl: ".category-carousel-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 5,
        },
        1500: {
          slidesPerView: 6,
        },
      }
    });

    $(".products-carousel").each(function() {
      var $el_id = $(this).attr('id');

      var products_swiper = new Swiper("#" + $el_id + " .swiper", {
        slidesPerView: 5,
        spaceBetween: 30,
        speed: 500,
        navigation: {
          nextEl: "#" + $el_id + " .products-carousel-next",
          prevEl: "#" + $el_id + " .products-carousel-prev",
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
          },
          768: {
            slidesPerView: 3,
          },
          991: {
            slidesPerView: 4,
          },
          1500: {
            slidesPerView: 5,
          },
        }
      });

    });

    // product single page
    var thumb_slider = new Swiper(".product-thumbnail-slider", {
      slidesPerView: 5,
      spaceBetween: 20,
      direction: "vertical",
      breakpoints: {
        0: {
          direction: "horizontal"
        },
        992: {
          direction: "vertical"
        },
      },
    });

    var large_slider = new Swiper(".product-large-slider", {
      slidesPerView: 1,
      spaceBetween: 0,
      effect: 'fade',
      thumbs: {
        swiper: thumb_slider,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
  }

  // Input spinner
  var initProductQty = function() {
    $('.product-qty').each(function() {
      var $el_product = $(this);
      var quantity = 0;

      $el_product.find('.quantity-right-plus').click(function(e) {
        e.preventDefault();
        quantity = parseInt($el_product.find('#quantity').val());
        $el_product.find('#quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function(e) {
        e.preventDefault();
        quantity = parseInt($el_product.find('#quantity').val());
        if (quantity > 0) {
          $el_product.find('#quantity').val(quantity - 1);
        }
      });

    });
  }

  // Jarallax
  var initJarallax = function() {
    jarallax(document.querySelectorAll(".jarallax"));
    jarallax(document.querySelectorAll(".jarallax-keep-img"), {
      keepImg: true,
    });
  }

  // Wishlist functionality
  var initWishlist = function() {
    function updateWishlistIcon(button, inWishlist) {
        const heartIcon = button.querySelector('.heart-icon');

        if (inWishlist) {
          // Add the 'active' class to visually indicate it's in the wishlist
          console.log('Product added to wishlist:', button.dataset.productId);
          button.classList.add('active');
          heartIcon.classList.add('text-danger'); // Change to your preferred color class
        } else {
          // Remove the 'active' class
          button.classList.remove('active');
          heartIcon.classList.remove('text-danger');
        }
    }

    document.addEventListener('click', function(event) {
        const wishlistButton = event.target.closest('.wishlist-btn');
        if (!wishlistButton) return; // Ignore clicks outside wishlist buttons

        event.preventDefault();
        console.log('Wishlist button clicked from script.js:', wishlistButton);

        const productId = wishlistButton.dataset.productId;
        const toggleWishlistUrl = wishlistButton.dataset.toggleUrl;
        const currentState = wishlistButton.dataset.inWishlist === 'true';
        const testString = 'This is a test string!';

        // Toggle UI state immediately for a better UX
        wishlistButton.dataset.inWishlist = (!currentState).toString();
        updateWishlistIcon(wishlistButton, !currentState);

        // Send AJAX request to update the server
        $.ajax({
            type: 'POST',
            url: toggleWishlistUrl, // Update this to your Django endpoint
            data: {
                product_id: productId,
                test_string: testString,
                action: 'post',
            },

            headers: {
              'X-CSRFToken': csrfToken,
            },

            success: function(response) {
                const newState = response.action === 'added';
                wishlistButton.dataset.inWishlist = newState.toString();
                updateWishlistIcon(wishlistButton, newState);

                if (newState) {
                  showToast('Product added to wishlist', 'success');
                } else {
                  showToast('Product removed from wishlist', 'info');
                }
            },
            error: function(xhr, errmsg, err) {
                // Revert UI state in case of an error
                wishlistButton.dataset.inWishlist = currentState.toString();
                updateWishlistIcon(wishlistButton, currentState);
                console.error('Error toggling wishlist:', errmsg);
                alert('Failed to update wishlist. Please try again later.');
            }
        });
    });
  };

  // Toast notification Function
  var showToast = function(message, type = 'primary') {
    // Get the toast element
    var toastEl = document.getElementById('liveToast');
    console.log('toast intitiated:', toastEl);

    // set the message and alert type
    toastEl.querySelector('.toast-body').textContent = message;
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;

    // show the toast element
    var toast = new bootstrap.Toast(toastEl);
    toast.show();
  };

  window.showToast = showToast;

  // Document ready
  $(document).ready(function() {
    initPreloader();
    initSwiper();
    initProductQty();
    initJarallax();
    initChocolat();
    initWishlist(); // Initialize the wishlist functionality
  });

})(jQuery);
