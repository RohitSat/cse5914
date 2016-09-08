const textInput = document.querySelector('#textInput');
const submitButton = document.querySelector('#submitButton');

const examples = {
  'What\'s one plus one?': 'One plus one is two!',
  'O-H': 'eye, oh',
  'What\'s the weather like in New York City?': 'The weather in New York is sunny or something.',
  'How many ounces in a gallon?': 'There are 128 fluid ounces in one gallon',
  'Why is the sky blue?': 'Because I said so',
}

const sayThing = (thing) => {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(thing);
  const engVoice = synth.getVoices()[3];
  utterance.voice = engVoice;
  synth.speak(utterance);
}

submitButton.addEventListener('click', (e) => {
  // sayThing(textInput.value);
  const response = examples[textInput.value] || 'I don\'t know how to answer that';
  sayThing(response);
});

// For the demo
Object.keys(examples).forEach(example => console.log(example));
