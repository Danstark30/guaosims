var first = document.querySelector('#number1');
var second = document.querySelector('#number2');
var result = document.querySelector('.result');
var firstb = document.querySelector('#number1b');
var secondb = document.querySelector('#number2b');
var resultb = document.querySelector('.resultb');
if (window.Worker) { //Chequea si el navegador soporta el api Worker
 // Creamos el worker con la ruta del script.
 var myWorker = new Worker("worker.js");
 var myWorkerb = new Worker("workerb.js")
 //Eventos para enviar el mensaje al worker.
 first.onchange = function() {    
  myWorker.postMessage([first.value,second.value]);  
  console.log('Message posted to worker'); 
 };
 firstb.onchange = function() {
  myWorkerb.postMessage([firstb.value,secondb.value]);
  console.log('Message posted to workerb');
 };
 second.onchange = function() {
  myWorker.postMessage([first.value,second.value]);
  console.log('Message posted to worker');
 };
  secondb.onchange = function() {
  myWorkerb.postMessage([firstb.value,secondb.value]);
  console.log('Message posted to workerb');
 };
 //Función onmessage para recibir los mensajes del worker
 myWorker.onmessage = function(e) {
  result.textContent = e.data;
  console.log('Message received from worker'); 
 };
  myWorkerb.onmessage = function(e) {
  resultb.textContent = e.data;
  console.log('Message received from workerb');
 };
}