/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/*.js","./src/**/*.js"],
  theme: {
    extend: {
      screens: {
      'mobile': '375px',
      }
    },
  },
  plugins: [],
}

