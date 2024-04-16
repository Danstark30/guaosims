var x = document.querySelector('x');
var y = document.querySelector('y');
if (window.Worker) { //Chequea si el navegador soporta el api Worker
 // Creamos el worker con la ruta del script.
 var myWorkerb = new Worker("workerb.js");
 //Eventos para enviar el mensaje al worker.
 function() {
  myWorkerb.postMessage([x.value,y.value]);
  console.log('Message posted to worker');
 };
 //Función onmessage para recibir los mensajes del worker
 myWorkerb.onmessage = function(e) {
  result.textContent = e.data;
  console.log('Message received from worker');
 };
}