
document.addEventListener('click',function(e){
  if(e.target.className.indexOf("editing") == -1 && e.target.className.indexOf("ocrx_cinfo") != -1){
    var oldEdit = document.querySelectorAll(".editing")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("editing");
    }
    var newEdit = e.target;
    newEdit.classList.add("editing");
    }
  else if(e.target.className.indexOf("ocr_page") != -1){

    var oldEdit = document.querySelectorAll(".editing")
    if (oldEdit.length > 0){
      oldEdit[0].classList.remove("editing");
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