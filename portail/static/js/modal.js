// modal.js
// Ce fichier gère l'affichage et le masquage des modales de résultat et de l'overlay de chargement.

const resultModal = document.getElementById('resultModal');
const modalHeader = document.getElementById('modalHeader');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const closeModalButton = document.getElementById('closeModalButton');
const closeModalFooterButton = document.getElementById('closeModalFooterButton');
const modalBackground = resultModal ? resultModal.querySelector('.modal-background') : null;

const loadingOverlay = document.getElementById('loadingOverlay');
const loadingMessage = document.getElementById('loadingMessage');

// Assurez-vous que les éléments de la modale existent avant d'ajouter des écouteurs
if (resultModal) {
    closeModalButton?.addEventListener('click', hideResultModal);
    closeModalFooterButton?.addEventListener('click', hideResultModal);
    modalBackground?.addEventListener('click', hideResultModal);
}

/**
 * Affiche la modale avec le titre, le message et le statut (succès/erreur).
 * @param {string} title - Le titre de la modale.
 * @param {string} message - Le message à afficher dans la modale.
 * @param {boolean} isSuccess - Vrai si l'opération a réussi, Faux sinon.
 */
export function showResultModal(title, message, isSuccess) {
    if (!resultModal || !modalTitle || !modalMessage || !modalHeader) {
        console.error("Erreur: Éléments de la modale non trouvés. Vérifiez index.html.");
        return;
    }

    modalTitle.textContent = title;
    modalMessage.textContent = message;

    // Réinitialise les classes de couleur sur le header de la modale
    modalHeader.classList.remove('is-success', 'is-danger');
    if (isSuccess) {
        modalHeader.classList.add('is-success'); // Pour la bordure teal
    } else {
        modalHeader.classList.add('is-danger'); // Pour la bordure rouge
    }

    resultModal.classList.add('is-active');
}

/**
 * Masque la modale de résultat.
 */
export function hideResultModal() {
    if (resultModal) {
        resultModal.classList.remove('is-active');
    }
}

/**
 * Affiche l'overlay de chargement avec un message optionnel.
 * @param {string} message - Le message à afficher sous le spinner.
 */
export function showLoadingOverlay(message = "Opération en cours...") {
    if (!loadingOverlay || !loadingMessage) {
        console.error("Erreur: Éléments de l'overlay de chargement non trouvés. Vérifiez index.html.");
        return;
    }
    loadingMessage.textContent = message;
    loadingOverlay.classList.add('is-active');
    // Désactiver les clics sur tous les boutons pendant le chargement
    document.querySelectorAll('a.button').forEach(btn => {
        btn.style.pointerEvents = 'none';
    });
}

/**
 * Masque l'overlay de chargement.
 */
export function hideLoadingOverlay() {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('is-active');
    }
    // Réactiver les clics sur tous les boutons
    document.querySelectorAll('a.button').forEach(btn => {
        btn.style.pointerEvents = 'auto';
    });
}
