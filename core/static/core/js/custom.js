class AdminSetup {

  /**
   * Setup global data
   */
  constructor() {

    // Get current page
    this.currentPage = document.querySelector('h1').textContent.toLowerCase().trim()
    console.log(this.currentPage)

    // Run methods in each page
    this.autorun()
  }


  /**
   * Run the functions for the current page
   */
  autorun() {
    // Methods to run for each page
    const methods = {
      // "imágenes de galería": [() => this.renderImages('.field-image a'), this.setupCopyButtons],
    }

    // Run the methods for the current page
    if (methods[this.currentPage]) {
      for (let method of methods[this.currentPage]) {
        method.call(this)
      }
    }
  }
}

new AdminSetup()