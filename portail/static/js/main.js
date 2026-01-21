// main.js: Script principal d'orchestration pour la gestion des ressources sur la page d'accueil.

import { trierRessources, filtrerParCategorie } from "./sort.js";
import { showResultModal, hideResultModal } from "./modal.js"; // Garder pour d'éventuels messages globaux
import { rechercher } from "./search.js";

// Variables globales pour stocker les ressources et les références aux éléments DOM.
const cardsContainer = document.getElementById("cardsContainer"); // Conteneur des cartes (div.columns)
let innerColumnsWrapper; // Référence au conteneur des cartes pour manipulation.
let carteElements = [];  // Liste des éléments HTML des cartes.
let ressources = [];     // Données structurées de chaque ressource.

// Exécute le code une fois que le DOM est entièrement chargé.
document.addEventListener('DOMContentLoaded', async () => {
    innerColumnsWrapper = cardsContainer;

    if (!innerColumnsWrapper) {
        // C'est normal si #cardsContainer n'est pas sur la page actuelle (ex: page de détail).
        // Ne pas logguer comme une erreur si c'est le cas.
        console.info("main.js: Le conteneur des cartes (#cardsContainer) n'a pas été trouvé. Ce script ne s'exécutera pas complètement sur cette page.");
        return; // Sortir si le conteneur n'est pas trouvé
    }

    // Récupère toutes les cartes et leurs données depuis le DOM.
    carteElements = Array.from(innerColumnsWrapper.children).filter(el => el.classList.contains('column'));
    ressources = carteElements.map(el => {
        const cardElement = el.querySelector('.card.resource-card');
        if (!cardElement) return null;
        return {
            element: el,
            title: cardElement.dataset.title || '',
            short_desc: cardElement.dataset.short_desc || '',
            icon: cardElement.dataset.icon || '',
            subjects: cardElement.dataset.subjects || '',
            packet_name: cardElement.dataset.packet_name || '',
            // isInstalled n'est plus nécessaire ici pour la page d'accueil
        };
    }).filter(r => r !== null);

    // Initialise le filtre par sujets (catégories).
    const subjectsFilter = document.getElementById('subjectsFilter'); 

    if (subjectsFilter) {
        if (!subjectsFilter.querySelector('option[value=""]')) {
            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Toutes les catégories";
            subjectsFilter.prepend(defaultOption); 
        }

        const uniqueSubjects = filtrerParCategorie(ressources, "");

        uniqueSubjects.forEach(cat => {
            if (!subjectsFilter.querySelector(`option[value="${cat}"]`)) {
                const option = document.createElement("option");
                option.value = cat;
                option.textContent = cat;
                subjectsFilter.appendChild(option);
            }
        });
    }

    const searchInput = document.getElementById('searchInput');
    const sortOrder = document.getElementById('sortOrder');

    searchInput?.addEventListener('input', applyFiltersAndSort);
    subjectsFilter?.addEventListener('change', applyFiltersAndSort); 
    sortOrder?.addEventListener('change', applyFiltersAndSort);

    // Les gestionnaires de modale restent ici car la modale de résultat peut être utilisée globalement
    document.getElementById('closeModalButton')?.addEventListener('click', hideResultModal);
    document.getElementById('closeModalFooterButton')?.addEventListener('click', hideResultModal);
    document.querySelector('#resultModal .modal-background')?.addEventListener('click', hideResultModal);

    // Applique les filtres et le tri au chargement initial de la page.
    applyFiltersAndSort();
});

// ## Applique les filtres et le tri
function applyFiltersAndSort() {
    const searchInput = document.getElementById('searchInput');
    const subjectsFilter = document.getElementById('subjectsFilter'); 
    const sortOrder = document.getElementById('sortOrder');

    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const selectedSubject = subjectsFilter ? subjectsFilter.value : ''; 
    const sortOrderValue = sortOrder ? sortOrder.value : 'none';

    let ressourcesAffiches = [...ressources];

    if (searchTerm) {
        ressourcesAffiches = rechercher(ressourcesAffiches, searchTerm);
    }

    if (selectedSubject) {
        ressourcesAffiches = filtrerParCategorie(ressourcesAffiches, selectedSubject);
    }

    if (sortOrderValue && sortOrderValue !== 'none') {
        ressourcesAffiches = trierRessources(ressourcesAffiches, sortOrderValue);
    }

    if (innerColumnsWrapper) {
        carteElements.forEach(el => el.style.display = 'none');

        const fragment = document.createDocumentFragment();
        ressourcesAffiches.forEach(r => {
            r.element.style.display = '';
            fragment.appendChild(r.element);
        });

        while (innerColumnsWrapper.firstChild) {
            innerColumnsWrapper.removeChild(innerColumnsWrapper.firstChild);
        }
        innerColumnsWrapper.appendChild(fragment);

        if (ressourcesAffiches.length === 0) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.className = 'has-text-centered has-text-grey is-size-5 mt-5';
            noResultsMessage.textContent = 'Aucun résultat trouvé.';
            innerColumnsWrapper.appendChild(noResultsMessage);
        }
    }
}