//Création des constantes à réutiliser
const reponseVide = "Tu voulais dire un truc peut-être ? Répond moi dans la zone de texte.";
const reponseFaux = "Attends. Je crois qu'il y a une erreur quelque part. Essaie de la corriger.";
const combinaisonCoffre = "MEETT";
const traductionMorse = "L Z P V J L F H I M L I M I M F M N I M P I M P I M A A I M A A I M A A I M A A I M P F H F Q F H L Z P M M P M N P J F H I M V F M N I M I M I M A A I M L I M V I M P I M P I M P I M P I M P I M P I M P I M P I M P I M P I M A B Q M";
const transformMorse = "0100 / 1100 / 0110 / 0001 / 0111 / 0100 / 0010 / 0000 / 00 / 11 / 0100 / 00 / 11 / 00 / 11 / 0010 / 11 / 10 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 01 / 01 / 00 / 11 / 01 / 01 / 00 / 11 / 01 / 01 / 00 / 11 / 01 / 01 / 00 / 11 / 0110 / 0010 / 0000 / 0010 / 1101 / 0010 / 0000 / 0100 / 1100 / 0110 / 11 / 11 / 0110 / 11 / 10 / 0110 / 0111 / 0010 / 0000 / 00 / 11 / 0001 / 0010 / 11 / 10 / 00 / 11 / 00 / 11 / 00 / 11 / 01 / 01 / 00 / 11 / 0100 / 00 / 11 / 0001 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 0110 / 00 / 11 / 01 / 1000 / 1101 / 11";
const traductionBinaire = "Lat 43.6655556 - Long 1.3541666666666667";

//Récupération des éléments de l'interface
/*let analyst = document.querySelector(".enonce");
let appelAnalyst = document.querySelector(".enonce__appel");
let indice = document.querySelector(".enonce__indice");*/
let coequipier = document.querySelector('.coequipier');
let message = document.querySelector('.coequipier__message');
let transmission = document.querySelector('.coequipier__morse');
let code = document.querySelector('.coequipier__transcription');
let container = document.querySelector('.coequiper__container');
let button = document.querySelector('.joueur__button');
let erreur = document.querySelector('.joueur__message');
let coffre = document.querySelector('.coffre__button');
let coffreAnswer = document.querySelector('.coffre__answer');
let alphabet;


//Création des fonctions
function createImg(){
    let img = document.createElement("img");
    img.setAttribute("alt","un alphabet d'encodage");
    img.classList.add("coequipier__alphabet");
    return img;
}

function verifPhase(answer,code){
    answer = answer.replaceAll(" ","").replaceAll("/","");
    code = code.replaceAll(" ","").replaceAll("/","").toLowerCase();
    return (answer == code);
}

function addClickToZoomImg(selecteur){
    let img = document.querySelector(selecteur);
    img.addEventListener('click',event => {
        container.classList.toggle("displayFlex");
        container.classList.toggle("zoom");
        container.classList.toggle("reduce");
    })
}

function addClickToReduceImg(){
    container.addEventListener('click',event => {
        container.classList.toggle("zoom");
        container.classList.toggle("reduce");
        setTimeout(()=>{container.classList.toggle("displayFlex")},1000);
    })
}

function phaseOne(){
    erreur.innerText = '';
    message.innerText = "Effectivement. Ca y ressemble bien. Tu penses pouvoir le traduire ? Voici sa transcription et l'alphabet Morse : ";
    code.innerText = ".-.. / --.. / .--. / ...- / .--- / .-.. / ..-. / .... / .. / -- / .-.. / .. / -- / .. / -- / ..-. / -- / -. / .. / -- / .--. / .. / -- / .--. / .. / -- / .- / .- / .. / -- / .- / .- / .. / -- / .- / .- / .. / -- / .- / .- / .. / -- / .--. / ..-. / .... / ..-. / --.- / ..-. / .... / .-.. / --.. / .--. / -- / -- / .--. / -- / -. / .--. / .--- / ..-. / .... / .. / -- / ...- / ..-. / -- / -. / .. / -- / .. / -- / .. / -- / .- / .- / .. / -- / .-.. / .. / -- / ...- / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .--. / .. / -- / .- / -... / --.- / --";
    alphabet = createImg();
    alphabet.setAttribute('src','./src/img/morse.png');
    container.append(alphabet);
    let thumb = createImg();
    thumb.setAttribute('src','./src/img/morse-thumbnail.png');
    thumb.setAttribute('class','coequipier__thumbnail');
    coequipier.append(thumb);
    button.classList.remove('phase0');
    button.classList.add('phase1');
    transmission.style.display = "none";
}

function phaseTwo(){
    erreur.innerText = '';
    message.innerText = "Mais... ça ne veut absoluement rien dire ! Cela doit cacher autre chose... J'ai une idée ! Essaie de remplacer les point par des 0, et les tirets par des 1. Ca donne quoi ?";
    button.classList.remove('phase1');
    button.classList.add('phase2');
}

function phaseThree(){
    erreur.innerText = '';
    message.innerText = "Ha ha ! Ca ressemble bien à du binaire. Le langage des oridnateurs. Ils me semblent que pour coder des lettres en binaire, il faut le faire par paquet de 8. C'est ce qu'on appelle un octet. Voici ce que ça donne, et voici l'alphabet ASCI. Peux-tu le traduire ?";
    code.innerText = "01001100 01100001 01110100 00100000 00110100 00110011 00101110 00110110 00110110 00110101 00110101 00110101 00110101 00110110 00100000 00101101 00100000 01001100 01101111 01101110 01100111 00100000 00110001 00101110 00110011 00110101 00110100 00110001 00110110 00110110 00110110 00110110 00110110 00110110 00110110 00110110 00110110 00110110 00110110 00110111";
    alphabet = document.querySelector('.coequipier__alphabet');
    alphabet.setAttribute('src','./src/img/ascii.png');
    let thumb = document.querySelector('.coequipier__thumbnail');
    thumb.setAttribute('src','./src/img/ascii-thumbnail.png');
    button.classList.remove('phase2');
    button.classList.add('phase3');
}

function phaseFour(){
    erreur.innerText = '';
    message.innerText = "Tiens donc. Ne serait-ce pas des coordonnées géographiques ? Je pense que si tu trouves l'endroit, tu trouves la combinaison du coffre.";
    button.classList.remove('phase2');
    button.classList.add('phase3');
}

function traducteurMorse(){
    let traducteur = document.createElement("iframe");
    traducteur.setAttribute("id","morse-decoder-iframe");
    traducteur.setAttribute('src',"https://embed.morsedecoder.com/fr/#-|.|%2F|%20|1|0.1|500|sine");
    traducteur.setAttribute('width',"100%");
    traducteur.setAttribute('height',"200");
    traducteur.setAttribute('style',"display: block; margin: 0px auto; border: 0px;");
    return traducteur;

}

//Initialisation du jeu
message.innerText = "Le code pour ouvrir le coffre est dissimulé dans cette transmission que l'on a intercepté. Je ne comprends pas très bien de quoi il s'agit. Quel code est utilisé d'après toi ?";

//Initialisation de l'analyste
/*appelAnalyst.addEventListener('click',event => {
    let traducteur = traducteurMorse();
    indice.innerText = "Bonjour. Voici un traducteur de code Morse pour vous aider";
    analyst.append(traducteur);
})*/

//Evolution du jeu : passage d'une phase à l'autre
button.addEventListener('click', event => {
    event.preventDefault();
    let interface = document.querySelector('#interface');
    const answer = interface.value.toLowerCase();
    switch(true){
        case button.classList.contains('phase0') && answer.includes('morse') :
            phaseOne();
            addClickToZoomImg('.coequipier__thumbnail');
            addClickToReduceImg();
            break;
        case button.classList.contains('phase1') && verifPhase(answer,traductionMorse):
            phaseTwo();
            break;
        case button.classList.contains('phase2') && verifPhase(answer,transformMorse):
            phaseThree();
            break;
        case button.classList.contains('phase3') && verifPhase(answer,traductionBinaire):
            phaseFour();
            break;
        case answer == "" :
            erreur.innerText = reponseVide;
            break;
        default :
            erreur.innerText = reponseFaux;
    }
    interface.value = '';
})

//Dévérouillage du Coffre
coffre.addEventListener('click', event => {
    event.preventDefault();
    let combinaison = document.querySelector('.coffre__combinaison');
    if(combinaison.value == combinaisonCoffre){
        coffreAnswer.innerText = "Félicitation, le coffre s'ouvre ! Le mot clé de ce flag est ENCODAGE ASCII";

    }else{
        coffreAnswer.innerText = "Le coffre reste vérouillé !";
    }

})