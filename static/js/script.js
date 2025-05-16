document.addEventListener("DOMContentLoaded", () => {
    // Check if custom cursor should be enabled
    const preferReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  
    if (!preferReducedMotion) {
      document.body.setAttribute("data-cursor", "true")
    }
  
    // Custom cursor
    const cursor = document.querySelector(".cursor")
    const cursorFollower = document.querySelector(".cursor-follower")
  
    // تغییر رفتار نشانگر ماوس در JavaScript
    // فعال کردن نشانگر ماوس سفارشی
    document.body.setAttribute("data-cursor", "true")
  
    // نشانگر ماوس سفارشی
    if (document.body.getAttribute("data-cursor") === "true") {
      document.addEventListener("mousemove", (e) => {
        cursor.style.left = e.clientX + "px"
        cursor.style.top = e.clientY + "px"
  
        setTimeout(() => {
          cursorFollower.style.left = e.clientX + "px"
          cursorFollower.style.top = e.clientY + "px"
        }, 50)
      })
  
      document.addEventListener("mousedown", () => {
        cursor.style.transform = "translate(-50%, -50%) scale(1.5)"
        cursorFollower.style.transform = "translate(-50%, -50%) scale(0.8)"
      })
  
      document.addEventListener("mouseup", () => {
        cursor.style.transform = "translate(-50%, -50%)"
        cursorFollower.style.transform = "translate(-50%, -50%)"
      })
  
      // افکت‌های هاور برای دکمه‌ها و لینک‌ها
      const interactiveElements = document.querySelectorAll(
        "button, a, .product-card, .category-card, .feature, input, .slider-arrow, .dot",
      )
  
      interactiveElements.forEach((element) => {
        element.addEventListener("mouseenter", () => {
          cursor.style.width = "15px"
          cursor.style.height = "15px"
          cursorFollower.style.width = "40px"
          cursorFollower.style.height = "40px"
        })
  
        element.addEventListener("mouseleave", () => {
          cursor.style.width = "10px"
          cursor.style.height = "10px"
          cursorFollower.style.width = "30px"
          cursorFollower.style.height = "30px"
        })
      })
    }
  
    // Initialize particles
    initParticles()
  
    // Parallax effect
    initParallax()
  
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
    const mainNav = document.querySelector(".main-nav")
  
    if (mobileMenuToggle) {
      mobileMenuToggle.addEventListener("click", () => {
        mainNav.classList.toggle("active")
      })
    }
  
    const hasSubmenu = document.querySelectorAll(".has-submenu")
  
    if (window.innerWidth <= 768) {
      hasSubmenu.forEach((item) => {
        const link = item.querySelector("a")
        const submenu = item.querySelector(".submenu")
  
        link.addEventListener("click", (e) => {
          e.preventDefault()
          if (submenu.style.display === "block") {
            submenu.style.display = "none"
          } else {
            submenu.style.display = "block"
          }
        })
      })
    }
  
    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll(".add-to-cart")
    const cartCount = document.querySelector(".cart-count")
    let count = Number.parseInt(cartCount.textContent)
  
    addToCartButtons.forEach((button) => {
      button.addEventListener("click", () => {
        count++
        cartCount.textContent = count.toLocaleString("fa-IR")
  
        // Animation effect
        const btnText = button.querySelector(".btn-text")
        const btnIcon = button.querySelector(".btn-icon")
  
        btnText.innerHTML =
          'افزوده شد <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        btnIcon.style.display = "none"
  
        // Add animation class
        button.classList.add("added-to-cart")
  
        setTimeout(() => {
          btnText.textContent = "افزودن به سبد"
          btnIcon.style.display = "block"
          button.classList.remove("added-to-cart")
        }, 1500)
  
        showToast("محصول به سبد خرید اضافه شد")
  
        // Create flying cart animation
        createFlyingElement(button, ".header-action.cart .icon-container")
      })
    })
  
    // Product action buttons
    const wishlistButtons = document.querySelectorAll(".product-action-btn.wishlist")
    const compareButtons = document.querySelectorAll(".product-action-btn.compare")
    const quickviewButtons = document.querySelectorAll(".product-action-btn.quickview")
  
    wishlistButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()
  
        // Toggle filled/unfilled heart icon
        const icon = button.querySelector(".icon")
        if (icon.getAttribute("fill") === "none") {
          icon.setAttribute("fill", "currentColor")
          showToast("محصول به علاقه‌مندی‌ها اضافه شد")
  
          // Create flying heart animation
          createFlyingElement(button, ".header-action:nth-child(2) .icon-container")
        } else {
          icon.setAttribute("fill", "none")
          showToast("محصول از علاقه‌مندی‌ها حذف شد")
        }
      })
    })
  
    compareButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()
        showToast("محصول به لیست مقایسه اضافه شد")
      })
    })
  
    quickviewButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()
        showToast("نمایش سریع محصول")
      })
    })
  
    // Back to top button
    const backToTopButton = document.querySelector(".back-to-top")
  
    window.addEventListener("scroll", () => {
      if (window.scrollY > 300) {
        backToTopButton.classList.add("visible")
      } else {
        backToTopButton.classList.remove("visible")
      }
    })
  
    backToTopButton.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      })
    })
  
    // Countdown timer
    const countdownItems = document.querySelectorAll(".countdown-number")
    const countdownCircles = document.querySelectorAll(".countdown-circle")
  
    if (countdownItems.length > 0) {
      // Set the countdown date (2 days from now)
      const countdownDate = new Date()
      countdownDate.setDate(countdownDate.getDate() + 2)
      countdownDate.setHours(18)
      countdownDate.setMinutes(45)
      countdownDate.setSeconds(33)
  
      function updateCountdown() {
        const now = new Date().getTime()
        const distance = countdownDate - now
  
        const days = Math.floor(distance / (1000 * 60 * 60 * 24))
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        const seconds = Math.floor((distance % (1000 * 60)) / 1000)
  
        // Update the countdown display
        countdownItems[0].textContent = days
          .toString()
          .padStart(2, "0")
          .replace(/\d/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
        countdownItems[1].textContent = hours
          .toString()
          .padStart(2, "0")
          .replace(/\d/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
        countdownItems[2].textContent = minutes
          .toString()
          .padStart(2, "0")
          .replace(/\d/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
        countdownItems[3].textContent = seconds
          .toString()
          .padStart(2, "0")
          .replace(/\d/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
  
        // Update circle animations
        if (countdownCircles.length > 0) {
          countdownCircles[0].style.strokeDashoffset = 283 - (283 * days) / 30
          countdownCircles[1].style.strokeDashoffset = 283 - (283 * hours) / 24
          countdownCircles[2].style.strokeDashoffset = 283 - (283 * minutes) / 60
          countdownCircles[3].style.strokeDashoffset = 283 - (283 * seconds) / 60
        }
  
        if (distance < 0) {
          clearInterval(countdownInterval)
        }
      }
  
      updateCountdown() // Run once immediately
      const countdownInterval = setInterval(updateCountdown, 1000)
    }
  
    // Parallax effect for hero section
    const heroSection = document.querySelector(".hero-slider")
    if (heroSection) {
      window.addEventListener("scroll", () => {
        const scrollPosition = window.scrollY
        if (scrollPosition < 600) {
          const slideImage = document.querySelector(".slide-image")
          if (slideImage) {
            slideImage.style.transform = `translateY(${scrollPosition * 0.1}px)`
          }
        }
      })
    }
  
    // 3D card effect
    const cards3D = document.querySelectorAll(".card-3d")
    cards3D.forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
  
        const centerX = rect.width / 2
        const centerY = rect.height / 2
  
        const rotateX = (y - centerY) / 10
        const rotateY = (centerX - x) / 10
  
        card.querySelector(".card-3d-content").style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
      })
  
      card.addEventListener("mouseleave", () => {
        card.querySelector(".card-3d-content").style.transform = "rotateX(0) rotateY(0)"
      })
    })
  
    // Initialize particles
    function initParticles() {
      const canvas = document.getElementById("particles")
      if (!canvas) return
  
      const ctx = canvas.getContext("2d")
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
  
      const particles = []
      const particleCount = 50
  
      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 2 + 1,
          color: `rgba(139, 92, 246, ${Math.random() * 0.5 + 0.1})`,
          speedX: Math.random() * 1 - 0.5,
          speedY: Math.random() * 1 - 0.5,
        })
      }
  
      function animate() {
        requestAnimationFrame(animate)
        ctx.clearRect(0, 0, canvas.width, canvas.height)
  
        particles.forEach((particle) => {
          ctx.beginPath()
          ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2)
          ctx.fillStyle = particle.color
          ctx.fill()
  
          particle.x += particle.speedX
          particle.y += particle.speedY
  
          if (particle.x < 0 || particle.x > canvas.width) {
            particle.speedX = -particle.speedX
          }
  
          if (particle.y < 0 || particle.y > canvas.height) {
            particle.speedY = -particle.speedY
          }
        })
      }
  
      animate()
  
      window.addEventListener("resize", () => {
        canvas.width = window.innerWidth
        canvas.height = window.innerHeight
      })
    }
  
    // Initialize parallax effect
    function initParallax() {
      const parallaxContainers = document.querySelectorAll(".parallax-container")
  
      parallaxContainers.forEach((container) => {
        const layers = container.querySelectorAll(".parallax-layer")
  
        container.addEventListener("mousemove", (e) => {
          const rect = container.getBoundingClientRect()
          const x = e.clientX - rect.left
          const y = e.clientY - rect.top
  
          const centerX = rect.width / 2
          const centerY = rect.height / 2
  
          layers.forEach((layer, index) => {
            const depth = index + 1
            const moveX = (x - centerX) / (10 * depth)
            const moveY = (y - centerY) / (10 * depth)
  
            layer.style.transform = `translate(${moveX}px, ${moveY}px)`
          })
        })
  
        container.addEventListener("mouseleave", () => {
          layers.forEach((layer) => {
            layer.style.transform = "translate(0, 0)"
          })
        })
      })
    }
  
    // Create flying element animation
    function createFlyingElement(sourceElement, targetSelector) {
      const source = sourceElement.getBoundingClientRect()
      const target = document.querySelector(targetSelector).getBoundingClientRect()
  
      const flyingElement = document.createElement("div")
      flyingElement.className = "flying-element"
      flyingElement.style.position = "fixed"
      flyingElement.style.width = "20px"
      flyingElement.style.height = "20px"
      flyingElement.style.backgroundColor = "var(--primary)"
      flyingElement.style.borderRadius = "50%"
      flyingElement.style.zIndex = "9999"
      flyingElement.style.opacity = "0.8"
      flyingElement.style.pointerEvents = "none"
  
      // Set initial position
      flyingElement.style.left = `${source.left + source.width / 2}px`
      flyingElement.style.top = `${source.top + source.height / 2}px`
  
      document.body.appendChild(flyingElement)
  
      // Animate to target
      flyingElement.animate(
        [
          {
            left: `${source.left + source.width / 2}px`,
            top: `${source.top + source.height / 2}px`,
            opacity: 0.8,
            transform: "scale(1)",
          },
          {
            left: `${target.left + target.width / 2}px`,
            top: `${target.top + target.height / 2}px`,
            opacity: 0,
            transform: "scale(0.2)",
          },
        ],
        {
          duration: 800,
          easing: "cubic-bezier(0.215, 0.61, 0.355, 1)",
        },
      ).onfinish = () => {
        flyingElement.remove()
  
        // Add pulse effect to target
        const targetElement = document.querySelector(targetSelector)
        targetElement.classList.add("pulse-glow")
        setTimeout(() => {
          targetElement.classList.remove("pulse-glow")
        }, 1000)
      }
    }
  
    // Toast notification
    function showToast(message) {
      // Create toast element if it doesn't exist
      let toast = document.querySelector(".toast")
      if (!toast) {
        toast = document.createElement("div")
        toast.className = "toast"
        document.body.appendChild(toast)
      }
  
      // Set message and show toast
      toast.textContent = message
      toast.classList.add("visible")
  
      // Hide toast after 3 seconds
      setTimeout(() => {
        toast.classList.remove("visible")
      }, 3000)
    }
  
    // Slider functionality
    const sliderDots = document.querySelectorAll(".slider-dots .dot")
    const sliderArrows = document.querySelectorAll(".slider-arrow")
  
    if (sliderDots.length > 0) {
      sliderDots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
          sliderDots.forEach((d) => d.classList.remove("active"))
          dot.classList.add("active")
          // Here you would add code to change the slide
        })
      })
    }
  
    if (sliderArrows.length > 0) {
      sliderArrows.forEach((arrow) => {
        arrow.addEventListener("click", () => {
          // Here you would add code to navigate slides
        })
      })
    }
  })
  
  