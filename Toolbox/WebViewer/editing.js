textEditInput = document.getElementById("textInput");

// selection

document.getElementsByClassName("hocr-viewer")[0].addEventListener('click',function(e){
  selectElement(e.target);
});

function selectElement(el){
  console.log(el);
  if(el.className.indexOf("selected") == -1 && el.className.indexOf("text_level_focus") != -1){
    var oldEdit = document.querySelectorAll(".selected")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("selected");
      //oldEdit[0].classList.add("edited")
    }
    var newEdit = el;
    newEdit.classList.add("selected");
    updatePropertyInterface(el)
  }
  else if(el.className.indexOf("ocr_page") != -1){
    var oldEdit = document.querySelectorAll(".selected")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("selected");
      //applyTransform2Bbox(oldEdit[0]);
    }
  }
}

function selectNext(){
  let el = document.getElementsByClassName("selected")[0];
  let next = getNext(el,0);
  selectElement(next);
}

function getNext(el, lvl){
  let next = el.nextElementSibling;
  if(next){
    return getFirstElementChildByLevel(next, lvl);
  }else{
    lvl += 1;
    return getNext(el.parentElement, lvl);
  }
}

function getFirstElementChildByLevel(el, lvl){
  if(lvl === 0){
    return el;
  }
  else{
    lvl -= 1;
    return getFirstElementChildByLevel(el.firstElementChild, lvl);
  }
}

function selectPrev(){
  let el = document.getElementsByClassName("selected")[0];
  let prev = getPrev(el,0);
  selectElement(prev);
}

function getPrev(el, lvl){
  let prev = el.previousElementSibling;
  if(prev){
    return getLastElementChildByLevel(prev, lvl);
  }else{
    lvl += 1;
    return getPrev(el.parentElement, lvl);
  }
}

function getLastElementChildByLevel(el, lvl){
  if(lvl === 0){
    return el;
  }
  else{
    lvl -= 1;
    return getLastElementChildByLevel(el.lastElementChild, lvl);
  }
}

function updatePropertyInterface(el){
  console.log(getText(el));
  textEditInput.value = getText(el);
}

function editText(){
  let elementSelected = document.getElementsByTagName("selected")[0];
  let newString = textEditInput.value;
  newString.split("\n\n");
}

// darg & resize


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

dragresize.isElement = function(elm){
 if (elm.className && elm.className.indexOf('selected') > -1 && editable) return true;
};
dragresize.isHandle = function(elm){
 if (elm.className && elm.className.indexOf('selected') > -1 && editable) return true;
};

// You can define optional functions that are called as elements are dragged/resized.
// Some are passed true if the source event was a resize, or false if it's a drag.
// The focus/blur events are called as handles are added/removed from an object,
// and the others are called as users drag, move and release the object's handles.
// You might use these to examine the properties of the DragResize object to sync
// other page elements, etc.

dragresize.ondragfocus = function() { console.log("focus"); };
dragresize.ondragstart = function(isResize) { console.log("start"); };
dragresize.ondragmove = function(isResize) {  };
dragresize.ondragend = function(isResize) {
  this.element.classList.add("edited");
  applyTransform2Bbox(this.element);
};
dragresize.ondragblur = function() { };

// Finally, you must apply() your DragResize object to a DOM node; all children of this
// node will then be made draggable. Here, I'm applying to the entire document.
dragresize.apply(document);
}

function removeElement(){
    var editingElement = document.querySelectorAll(".selected")
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
    removeAllDragresize();
    removeStyles(newHOCR);
    //console.log(newHOCR.outerHTML)
    newHTML = currentHOCR.cloneNode(true)

    newHTML.body.innerHTML = newHOCR.outerHTML;

    download(newHTML.documentElement.outerHTML,"p"+     String(page)+".hocr","html")

    //console.log(currentHOCR)


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

    function removeAllDragresize(){
      let elements = document.getElementsByClassName("dragresize");
      for (var i = 0; i < elements.length; i++) {
        console.log(elements[i]);
        elements[i].parentNode.removeChild(elements[i]);
        console.log(elements[i]);
        elements[i].remove()
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

resize();

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

function adjust_bbox_from_children(el){
  let children = el.children;
  if(children.length > 0){
    let all_x0 = [], all_y0 = [], all_x1 = [], all_y1 = [];
    for (var i = 0; i < children.length; i++) {
      if (isHocrElement(children[i])){
        let bbox = getTitleAttribute(children[i], "bbox");
        let x0, y0, x1, y1;
        [x0, y0, x1, y1] = bbox;
        console.log(x0, y0, x1, y1);
        all_x0.push(x0);
        all_y0.push(y0);
        all_x1.push(x1);
        all_y1.push(y1);
      }
    }
    console.log(all_x0, all_y0, all_x1, all_y1);
    // calculate bbox
    let min_x0 = Math.min(...all_x0); // oui... cette syntaxe existe, c'est du destructuring assignment
    let min_y0 = Math.min(...all_y0);
    let max_x1 = Math.max(...all_x1);
    let max_y1 = Math.max(...all_y1);
    console.log(min_x0,min_y0,max_x1,max_y1);
    // apply bbox to CSS
    bbox2css(element, [min_x0, min_y0, max_x1, max_y1]);
    // apply CSS to Title Attribute
    applyTransform2Bbox(el);
  }else{
    console.log("children not found");
  }
}

function adjust_bbox_from_parent(element){
  let parent = element.parentElement;
  if(parent && isHocrElement(parent)){
    let parent_bbox = getTitleAttribute(parent,"bbox");
    let bbox = getTitleAttribute(element, "bbox");
    new_x0 = Math.max(parent_bbox[0], bbox[0]);
    new_y0 = Math.max(parent_bbox[1], bbox[1]);
    new_x1 = Math.min(parent_bbox[2], bbox[2]);
    new_y1 = Math.min(parent_bbox[3], bbox[3]);
    bbox2css(element, [new_x0, new_y0, new_x1, new_y1]);
    applyTransform2Bbox(element)
  }
}
