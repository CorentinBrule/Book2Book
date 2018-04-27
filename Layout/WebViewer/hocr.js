var list_ocr_tag = ["ocr_page","ocr_carea","ocr_par","ocr_line","ocrx_word","ocrx_cinfo"];
var debPage = 336;
var finPage = 356;

var page = 0;
var hash;
var targetHash="";
var pageHash="";
var zoomSlider = document.querySelector('.zoom');
var zoomValue = parseInt(zoomSlider.value);

var selector = document.querySelector("#selectPage");

var cbborders = document.getElementsByClassName("cbborders")
var cbimages = document.getElementsByClassName("cbimages")

window.onhashchange = function() {
    updateWithHash();
}

document.addEventListener('keypress', (event) => {
  const nomTouche = event.key;
  console.log(nomTouche)
  if (event.altKey){
      switch (nomTouche) {
        case "+":
            zoomValue+=2;
            updateZoom();
            break;
        case "-":
            zoomValue-=2;
            updateZoom();
            break;
        case "i":
            imageState = !imageState;
            updateImage();
            break;
        case "Delete":
            removeElement();
        }
    }
});

function updateWithHash(){
    hash = location.hash;
    if (hash.length >1){

        if (hash.indexOf("-") != -1){
            pageHash = parseInt(hash.split("-")[0].slice(1));
            targetHash = hash.split("-")[1];
        }else{
            targetHash = hash.slice(1);
        }

        if (pageHash != page){
            page = pageHash;
            loadFile(page);
            updateSelector();
            selector.value = page;
        }
        console.log(page)
        if (page == 0){
            page = debPage
            loadFile(page)
        }else{
            location.hash = targetHash;
            console.log(targetHash,page);
        }
    }else{
        if (page == 0){
            page = debPage
            loadFile(page)
        }
    }
}

for (var ipage = debPage; ipage < finPage + 1; ipage++) {
    var option = document.createElement('option');
    option.value = ipage;
    option.textContent = "page n°" + ipage;
    selector.appendChild(option);
    /*
    if (ipage == debPage) {
        option.selected = "selected"
        loadFile(page);
    }*/
}
updateWithHash();

document.querySelector("#selectPage").addEventListener('change', function() {
    loadFile(this.value);
    console.log(this.value)
});

function updateTarget(){
    newTarget = document.getElementById(targetHash);
    console.log(newTarget);
    location.hash = targetHash;
    xTarget = newTarget.style.left.slice(0,-2);
    xScroll = xTarget - document.getElementsByTagName("body")[0].clientWidth/2
    window.scrollTo(xScroll,window.scrollY)
}

function updateSelector(){
    for( var i = 0; i < selector.options.length; i++){
        if (selector.options[i].value == page){
            selector.options[i].selected = "selected"
        }
    }
}

function updateFromMenu(){
    for (var i=0 ; i < cbborders.length ; i++){
        checkBorders(cbborders[i])
    }
}

function loadFile(page) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            functHOCR(xhttp);
        }
    };
    xhttp.open("GET", "/Layout/hocr-charboxes/p" + page + ".hocr", true);
    xhttp.send();
}

var imageState = true;
var cbImage = document.getElementById("checkboxImage");
function checkImage(self) {
    var div = self.value;
    console.log(imageState,self.checked)
    imageState = self.checked;
    updateImage();
}

function updateImage(){
    cbImage.checked = imageState;
    if (imageState) {
        document.querySelector("."+cbImage.value).style.backgroundSize = "auto";
    } else {
        document.querySelector("."+cbImage.value).style.backgroundSize = "0 0";
    }
}

function checkBorders(self) {
    var divs = document.querySelectorAll("." + self.value);
    var len = divs.length;
    if (self.checked) {
        for (i = 0; i < len; i++) {
            divs[i].style.outlineStyle = "solid";
        }
    } else {
        for (i = 0; i < len; i++) {
            divs[i].style.outlineStyle = "none";
        }
    }
}

function checkText(self) {
  var oldDivs = document.querySelectorAll(".text_level_focus");
  var len = oldDivs.length;
  var i = 0;
  console.log(len);
  console.log(oldDivs[oldDivs.length-1]);
  for(i; i < len ; i++){
    console.log(oldDivs[i]);
    oldDivs[i].classList.remove("text_level_focus");
  }

  var divs = document.querySelectorAll("." + self.value);
  var len = divs.length;
  i=0;
  for (var i = 0; i < len; i++) {
    divs[i].classList.add("text_level_focus");
    if (divs[i].className.indexOf("ocrx_cinfo") == -1 ){
        divs[i].setAttribute("text-content",divs[i].textContent);
    }else{
    }
  }
}
/*
(function checkFocus() {
    focus = document.querySelectorAll(".cbFocus");
    for (var i = 0; i < focus.length; i++) {
        focus[i].addEventListener("click", function(e) {
            var TRs = document.querySelectorAll(".TextRegion");
            var TLs = document.querySelectorAll(".TextLine");
            var Ws = document.querySelectorAll(".Word");
            var Gs = document.querySelectorAll(".Glyph");
            var all = [TRs, TLs, Ws, Gs];
            var id = e.target.id[2];

            for (var j = 0; j < all.length; j++) {
                for (var k = 0; k < all[j].length; k++) {
                    if (id == j) {
                        all[j][k].style.pointerEvents = "auto";
                    } else {
                        all[j][k].style.pointerEvents = "none";
                    }
                }
            }
            //console.log(id);
        });
    }
})();
*/
zoomSlider.addEventListener('input', function(ev) {
    zoomValue = parseInt(ev.target.value);
    updateZoom();
  // console.log();
});

function updateZoom(){
  console.log(zoomValue)
  zoomSlider.value = zoomValue;
  var scaleFactor = zoomValue / 100.0;
  var page = document.querySelector('.ocr_page');
  page.style.transform = 'scale(' + scaleFactor + ')';
  page.style.transformOrigin = 'top left';
}

var fontSlider = document.querySelector('.fontSize');
fontSlider.addEventListener('input', function(ev) {
  var scaleFactor = ev.target.value / 10;
  var textDiv = document.querySelector('.'+list_ocr_tag[0]);
  textDiv.style.fontSize = scaleFactor+"em";
  // console.log();
});
/*
function generateMenu(hocrDoc){
  menu = document.getElementById("menu");
  menu_html = ""
  firstPage = hocrDoc.querySelector(".ocr_page");
  if (getTitleAttribute(firstPage,"image")!= null ){
    menu_html += '<input id="checkboxImage" type="checkbox" value="'+firstPage.id+'" checked="True" onchange="checkImage(this)">Image<br>'
  }
  var i = 0;
  var len = list_ocr_tag.length;
  for (i;i<len;i++){
    tag = list_ocr_tag[i];
    all_elements_by_tag = hocrDoc.getElementsByClassName(tag);
    if (all_elements_by_tag.length > 0){
      menu_html += '<input id="cbBorders'+tag+'" type="checkbox" value="'+tag+'" checked="True" onchange="checkBorders(this)">Text Regions<br>'
    }
  }
}
*/
function getTitleAttribute(hocr_element,attribute){
  title = hocr_element.getAttribute("title");
  if (attribute ==  'bbox' || attribute == "x_bboxes"){
    try{
      return title.match(/bbox\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/).slice(1).map(function(coord) {
        return parseInt(coord);
      });
    }catch(e){ // hocr specification says ocrx_cinfo has x_bboxes attribute instead of bbox
      return title.match(/x_bboxes\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/).slice(1).map(function(coord) {
        return parseInt(coord);
      });
    }
  }
  else if (attribute == 'image') {
    return title.match(/image\s+"([^"]+)"/)[1];
  }
  else if (attribute == null) {
    return title;
  }
}

function placeOcrElements(element) {
  var coords = getTitleAttribute(element,"bbox");
  //console.log(element);
  element.style.left = coords[0] + "px";
  element.style.top = coords[1] + "px";
  element.style.width = coords[2] - coords[0] + "px";
  element.style.height = coords[3] - coords[1] + "px";
  var page_coords = getTitleAttribute(document.querySelector('.ocr_page'),"bbox");
  document.querySelector('body').style.minHeight = page_coords[2] + 'px';
}

function functHOCR(xhttp) {
    var response = xhttp["response"];
    parser = new DOMParser();
    hocrDoc = parser.parseFromString(response, "text/html");

    //generateMenu(hocrDoc)

    //console.log(hocrDoc.body.innerHTML);
    firstPage = hocrDoc.querySelector(".ocr_page"); //ne fonctionne que pour une page par document hocr

    imgpath = "/" + getTitleAttribute(firstPage,"image");
    firstPage.style.backgroundImage = "url("+imgpath+")"

    layoutdiv = document.querySelector('.hocr-viewer');
    layoutdiv.innerHTML = firstPage.parentNode.innerHTML;

    //console.log(firstPage);
    ocr_page = document.querySelector('.ocr_page');

    var i = 0;

    for (i;i<list_ocr_tag.length;i++){
      var j = 0;
      var ls = document.querySelectorAll("."+list_ocr_tag[i]);
      var len = ls.length;
      for (j ; j < len ; j++){
        placeOcrElements(ls[j]);
      }
    }


    if (targetHash.length>1){
        updateTarget();
    }


    updateFromMenu();
    updateZoom();
}
