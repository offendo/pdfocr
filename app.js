const {MathpixMarkdownModel} = require('mathpix-markdown-it');

const Window = require('window');
const window = new Window();
global.window = window;
global.document = window.document;

const jsdom = require("jsdom");
const { JSDOM } = jsdom;
global.DOMParser = new JSDOM().window.DOMParser;

const fs = require('node:fs');
fs.readFile('Abstract+Algebra.mmd', 'utf8', (err, text) => {
  if (err) {
    console.error(err);
    return;
  }
  const options = {
    htmlTags: true,
    width: 800,
  };
  const htmlMM = MathpixMarkdownModel.markdownToHTML(text, options);
  
  console.log(htmlMM);
});
