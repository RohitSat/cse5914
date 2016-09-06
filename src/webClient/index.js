const postURL = 'http://requestb.in/1kfz7hq1';
const textInput = document.querySelector('#textInput');
const submitButton = document.querySelector('#submitButton');

const sayThing = (thing) => {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(thing);
  const engVoice = synth.getVoices()[3];
  utterance.voice = engVoice;
  synth.speak(utterance);
}

submitButton.addEventListener('click', (e) => {
  sayThing(textInput.value);
  if (textInput.value === 'What\'s one plus one?') {
    sayThing('One plus one is two!');
  }
});
