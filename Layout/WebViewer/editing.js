// drag resize

document.addEventListener('click',function(e){
  if(e.target.className.indexOf("editing") == -1 && e.target.className.indexOf("ocrx_cinfo") != -1){
    var oldEdit = document.querySelectorAll(".editing")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("editing");
      oldEdit[0].classList.add("edited")
    }
    var newEdit = e.target;
    newEdit.classList.add("editing");
    }
  else if(e.target.className.indexOf("ocr_page") != -1){

    var oldEdit = document.querySelectorAll(".editing")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("editing");
      oldEdit[0].classList.add("edited")
      //applyTransform2Bbox(oldEdit[0]);
    }
  }
});

resize();

// Using DragResize is simple!
// You first declare a new DragResize() object, passing its own name and an object
// whose keys constitute optional parameters/settings:
/*
document.addEventListener('keypress', (event) => {
  const nomTouche = event.key;
  console.log(nomTouche)
  if (event.altKey){
      switch (nomTouche) {
        case "r":
          resize();
          break;
        case "s":
          stopResize();
          break;
      }
  }
});
*/
var dragresize = null;

function stopResize(){

}

function resize(){
  dragresize = new DragResize('dragresize',
 { minWidth: 1, minHeight: 1 });

// Optional settings/properties of the DragResize object are:
//  enabled: Toggle whether the object is active.
//  handles[]: An array of drag handles to use (see the .JS file).
//  minWidth, minHeight: Minimum size to which elements are resized (in pixels).
//  minLeft, maxLeft, minTop, maxTop: Bounding box (in pixels).

// Next, you must define two functions, isElement and isHandle. These are passed
// a given DOM element, and must "return true" if the element in question is a
// draggable element or draggable handle. Here, I'm checking for the CSS classname
// of the elements, but you have have any combination of conditions you like:

dragresize.isElement = function(elm)
{
 if (elm.className && elm.className.indexOf('editing') > -1) return true;
};
dragresize.isHandle = function(elm)
{
 if (elm.className && elm.className.indexOf('editing') > -1) return true;
};

// You can define optional functions that are called as elements are dragged/resized.
// Some are passed true if the source event was a resize, or false if it's a drag.
// The focus/blur events are called as handles are added/removed from an object,
// and the others are called as users drag, move and release the object's handles.
// You might use these to examine the properties of the DragResize object to sync
// other page elements, etc.

dragresize.ondragfocus = function() { };
dragresize.ondragstart = function(isResize) { };
dragresize.ondragmove = function(isResize) { };
dragresize.ondragend = function(isResize) { };
dragresize.ondragblur = function() { };

// Finally, you must apply() your DragResize object to a DOM node; all children of this
// node will then be made draggable. Here, I'm applying to the entire document.
dragresize.apply(document);
}

function removeElement(){
    var editingElement = document.querySelectorAll(".editing")
    if (editingElement.length > 0){
      editingElement[0].parentNode.removeChild(editingElement[0])
    }
}

// save edition

function saveEdition(){
    var newHTML = document.documentElement.cloneNode(true)
    var newHOCR = newHTML.querySelector(".hocr-viewer")
    //console.log(newHOCR)
    var editedElements = newHOCR.querySelectorAll(".edited");

    var i = 0;
    for (i ; i<editedElements.length ; i++){
        applyTransform2Bbox(editedElements[i]);
    }
    removeStyles(newHOCR);
    //console.log(newHOCR.outerHTML)
    newHTML = currentHOCR.cloneNode(true)

    newHTML.body.innerHTML = newHOCR.outerHTML;

    download(newHTML.documentElement.outerHTML,"p"+String(page)+".hocr","html")

    //console.log(currentHOCR)

    function applyTransform2Bbox(element){
        l = element.style.left.split("px")[0];
        t = element.style.top.split("px")[0];
        w = String(parseInt(element.style.width.split("px")[0])+parseInt(l));
        h = String(parseInt(element.style.height.split("px")[0])+parseInt(t));
        oldTitle = element.getAttribute("title");
        //var reReplace = new RegExp(/$1 / + l + / / + t + / / + w + / / + + h ,"g");
        newTitle = oldTitle.replace(/(bbox|x_bboxes)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/,"$1 " + l + " " + t + " " + w + " "  + h)
        element.setAttribute("title",newTitle)
    }
    function removeStyles(el) {

        el.removeAttribute('style');

        if(el.childNodes.length > 0) {
            for(var child in el.childNodes) {
                /* filter element nodes only */
                if(el.childNodes[child].nodeType == 1)
                    removeStyles(el.childNodes[child]);
                }
            }
        }

    function download(data, filename, type) {
        var file = new Blob([data], {type: type});
        if (window.navigator.msSaveOrOpenBlob) // IE10+
            window.navigator.msSaveOrOpenBlob(file, filename);
        else { // Others
            var a = document.createElement("a"),
                    url = URL.createObjectURL(file);
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 0);
        }
    }
}