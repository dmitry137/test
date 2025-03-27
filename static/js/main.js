document.addEventListener("DOMContentLoaded", () => {
  // Add animation to elements when they appear in viewport
  const animateOnScroll = () => {
    const elements = document.querySelectorAll(".campaign-card, .form-section, .auth-card")

    elements.forEach((element) => {
      const elementTop = element.getBoundingClientRect().top
      const elementBottom = element.getBoundingClientRect().bottom

      // Check if element is in viewport
      if (elementTop < window.innerHeight && elementBottom > 0) {
        element.style.animation = "fadeIn 0.6s ease-out forwards"
      }
    })
  }

  // Run on page load
  animateOnScroll()

  // Run on scroll
  window.addEventListener("scroll", animateOnScroll)

  // Form validation
  const forms = document.querySelectorAll("form")

  forms.forEach((form) => {
    const emailInputs = form.querySelectorAll('input[type="email"]')

    emailInputs.forEach((input) => {
      input.addEventListener("blur", function () {
        const value = this.value.trim()

        if (value && !isValidEmail(value)) {
          this.classList.add("error")

          // Add error message if it doesn't exist
          let errorMessage = this.nextElementSibling
          if (!errorMessage || !errorMessage.classList.contains("error-message")) {
            errorMessage = document.createElement("div")
            errorMessage.className = "error-message"
            errorMessage.style.color = "var(--danger-color)"
            errorMessage.style.fontSize = "0.75rem"
            errorMessage.style.marginTop = "0.25rem"
            this.parentNode.insertBefore(errorMessage, this.nextSibling)
          }

          errorMessage.textContent = "Пожалуйста, введите корректный email адрес"
        } else {
          this.classList.remove("error")

          // Remove error message if it exists
          const errorMessage = this.nextElementSibling
          if (errorMessage && errorMessage.classList.contains("error-message")) {
            errorMessage.remove()
          }
        }
      })
    })

    // Validate form on submit
    form.addEventListener("submit", (event) => {
      let hasError = false

      // Validate required fields
      const requiredInputs = form.querySelectorAll("input[required], select[required], textarea[required]")

      requiredInputs.forEach((input) => {
        if (!input.value.trim()) {
          input.classList.add("error")
          hasError = true

          // Add error message if it doesn't exist
          let errorMessage = input.nextElementSibling
          if (!errorMessage || !errorMessage.classList.contains("error-message")) {
            errorMessage = document.createElement("div")
            errorMessage.className = "error-message"
            errorMessage.style.color = "var(--danger-color)"
            errorMessage.style.fontSize = "0.75rem"
            errorMessage.style.marginTop = "0.25rem"
            input.parentNode.insertBefore(errorMessage, input.nextSibling)
          }

          errorMessage.textContent = "Это поле обязательно для заполнения"
        } else {
          input.classList.remove("error")

          // Remove error message if it exists
          const errorMessage = input.nextElementSibling
          if (errorMessage && errorMessage.classList.contains("error-message")) {
            errorMessage.remove()
          }
        }
      })

      // Validate email fields
      emailInputs.forEach((input) => {
        const value = input.value.trim()

        if (value && !isValidEmail(value)) {
          input.classList.add("error")
          hasError = true

          // Add error message if it doesn't exist
          let errorMessage = input.nextElementSibling
          if (!errorMessage || !errorMessage.classList.contains("error-message")) {
            errorMessage = document.createElement("div")
            errorMessage.className = "error-message"
            errorMessage.style.color = "var(--danger-color)"
            errorMessage.style.fontSize = "0.75rem"
            errorMessage.style.marginTop = "0.25rem"
            input.parentNode.insertBefore(errorMessage, input.nextSibling)
          }

          errorMessage.textContent = "Пожалуйста, введите корректный email адрес"
        }
      })

      if (hasError) {
        event.preventDefault()

        // Scroll to first error
        const firstError = form.querySelector(".error")
        if (firstError) {
          firstError.scrollIntoView({ behavior: "smooth", block: "center" })
          firstError.focus()
        }
      }
    })
  })

  // Email validation helper
  function isValidEmail(email) {
    const re =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return re.test(String(email).toLowerCase())
  }

  // Add input styles for focus and error states
  const inputs = document.querySelectorAll("input, select, textarea")

  inputs.forEach((input) => {
    // Add focus styles
    input.addEventListener("focus", function () {
      this.style.borderColor = "var(--primary-color)"
      this.style.boxShadow = "0 0 0 3px rgba(99, 102, 241, 0.2)"
    })

    input.addEventListener("blur", function () {
      if (!this.classList.contains("error")) {
        this.style.borderColor = "var(--border-color)"
        this.style.boxShadow = "none"
      }
    })
  })

  // Add hover effects to buttons
  const buttons = document.querySelectorAll(".btn")
  buttons.forEach((button) => {
    button.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-2px)"
    })

    button.addEventListener("mouseleave", function () {
      this.style.transform = ""
    })
  })
})

