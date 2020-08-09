
var toggle=0;
//-----------------------modal window activation---------------------//
var modal = document.getElementById('myModal');
var hold=document.getElementById("holder");
// Get the image and insert it inside the modal - use its "alt" text as a caption
var form_img = document.getElementById('upload');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var area= document.getElementById('sub-area');
area.onclick = function(){
    modal.style.display = "block";
    modalImg.src = form_img.src;
    captionText.innerHTML = form_img.alt;
}


// Get the <span> element that closes the modal
var close = document.getElementsByClassName("close")[0];
var close1 = document.getElementsByClassName("close-btn")[0];

// When the user clicks on <span> (x), close the modal
close.onclick = function() { 
    modal.style.display = "none";
}
close1.onclick = function() { 
    toggle=0;
    document.getElementById("modal-crop-btn").style.color="black";
    modal.style.display = "none";
}

//----------------------------------modal-window-closed----------------------------//
document.getElementById("img01").addEventListener("wheel",zoomfunction());
function zoomfunction(e){

//-----------------to do zoomin and zoomout on ousewheel-------------------------
}



function zoom(zm){  //for zooming in and out with help of buttons
img=document.getElementById("img01");
wid=img.width;
ht=img.height;
if(wid*zm<100 || ht*zm<100 ){
    return;}
    else{
img.style.width=(wid*zm)+"px";
img.style.height=(ht*zm)+"px";}
     }


//--------------for image panning--------------------------------//

        //------if users select region other than in crop area than allow image panning---------//

document.getElementById('img01').addEventListener('mousedown', start_drag);
                  
function start_drag(e) {
  if(toggle==0){
  img_ele = this;
  x_img_ele = e.clientX - document.getElementById('img01').offsetLeft - 8;
  y_img_ele = e.clientY - document.getElementById('img01').offsetTop - 8;
                }
                else return;}
       
                        

document.getElementById('holder').addEventListener('mousemove', while_drag);
function while_drag(e) {
  if(toggle==0){
  var x_cursor = e.clientX;
  var y_cursor = e.clientY;
  if (img_ele !== null)     {
    img_ele.style.left = (x_cursor - x_img_ele) + 'px';
    img_ele.style.top = ( e.clientY - y_img_ele) + 'px';
                }
        else return;
                }
 //     console.log(img_ele.style.left+' - '+img_ele.style.top+"dragged");

                            
                        }
  
document.getElementById('holder').addEventListener('mouseup', stop_drag);
function stop_drag(e) {
  if(toggle==0){
  img_ele = null;
               }
               else return;
             }

                 
        
                       

//------------------------------------------------------------------//
//-----------function to change the value of toggle to '1' to enable cropbox function and stop image panning-----------------//
function cropbox(){
toggle=1;
document.getElementById("modal-crop-btn").style.color="blue";

}

if(toggle==1){}
    