// static/js/resourceDetail.js: Script spécifique à la page de détail d'une ressource.

// Importe les fonctions du module modal.js.
import { showResultModal, hideResultModal, showLoadingOverlay, hideLoadingOverlay } from "./modal.js";

// Cette variable stockera les informations de la ressource affichée.
let currentResource = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Récupérer les boutons d'action.
    const installButton = document.querySelector('.button.is-install');
    const uninstallButton = document.querySelector('.button.is-uninstall');
    const launchButton = document.querySelector('.button.is-launch');

    // S'assurer que nous sommes sur la page de détail et que des boutons d'action existent.
    if (!installButton && !uninstallButton && !launchButton) {
        console.warn("resourceDetail.js: Aucun bouton d'action trouvé sur cette page.");
        return;
    }

    // Déclarer packageName une seule fois.
    let packageName;

    // Récupérer le nom du paquet depuis l'attribut data-packet-name d'un des boutons.
    // L'accès aux attributs data- se fait en camelCase (data-packet-name devient .dataset.packetName).
    if (installButton) {
        packageName = installButton.dataset.packetName;
    } else if (uninstallButton) {
        packageName = uninstallButton.dataset.packetName;
    } else if (launchButton) {
        packageName = launchButton.dataset.packetName;
    } else {
        packageName = null; // Aucuns boutons trouvés, donc pas de packageName.
    }

    if (!packageName) {
        console.warn("resourceDetail.js: Attribut data-packet-name manquant sur les boutons d'action. Les actions ne seront pas disponibles.");
        return;
    }

    // Initialiser l'objet currentResource.
    currentResource = {
        packet_name: packageName,
        isInstalled: 'unknown' // Initialisation de l'état.
    };

    // Attacher les gestionnaires d'événements initiaux (seront mis à jour par updateButtonsState).
    if (installButton) installButton.onclick = () => sendAction('install', packageName);
    if (uninstallButton) uninstallButton.onclick = () => sendAction('uninstall', packageName);
    if (launchButton) launchButton.onclick = () => sendAction('launch', packageName);

    // Initialiser l'état des boutons au chargement de la page.
    await checkAndUpdatePackageState();
});

// Envoie une action au backend (install, uninstall, launch).
async function sendAction(action, packageName) {
    console.log(`Sending ${action} request for: ${packageName}`);
    showLoadingOverlay(`Exécution de la commande '${action}' pour '${packageName}'...`);
    
    try {
        const response = await fetch(`/admin/api/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ packet_name: packageName }),
        });
        const data = await response.json();
        hideLoadingOverlay();
        showResultModal(data.success ? 'Succès' : 'Échec', data.message);

        // Après une installation/désinstallation, mettez à jour l'état du paquet.
        if (action === 'install' || action === 'uninstall') {
            await checkAndUpdatePackageState(); // Re-vérifier l'état et mettre à jour les boutons.
        }
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error:', error);
        showResultModal('Erreur', `Une erreur réseau est survenue lors de l'opération ${action}.`);
    }
}

// Vérifie l'état d'installation du paquet et met à jour les boutons.
async function checkAndUpdatePackageState() {
    if (!currentResource || !currentResource.packet_name) {
        return;
    }
    
    const packageName = currentResource.packet_name;
    try {
        const response = await fetch(`/admin/api/check_package_state?packet_name=${encodeURIComponent(packageName)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        currentResource.isInstalled = data.is_installed; // Mettre à jour l'état dans l'objet global.

        updateActionButtonsState(); // Mettre à jour l'affichage des boutons.
        return data.is_installed;
    } catch (error) {
        console.error(`Erreur lors de la vérification de l'état de ${packageName}:`, error);
        currentResource.isInstalled = 'unknown'; // Marquer comme inconnu en cas d'erreur.
        updateActionButtonsState(); // Mettre à jour l'affichage des boutons même en cas d'erreur.
        return 'unknown';
    }
}

// Met à jour l'affichage des boutons d'action.
function updateActionButtonsState() {
    const installButton = document.querySelector('.button.is-install');
    const uninstallButton = document.querySelector('.button.is-uninstall');
    const launchButton = document.querySelector('.button.is-launch');

    if (!currentResource || !currentResource.packet_name) {
        console.warn("updateActionButtonsState: currentResource ou packet_name manquant.");
        return;
    }

    const packageName = currentResource.packet_name;

    // Réinitialiser les gestionnaires de clic pour éviter les doublons.
    if (installButton) installButton.onclick = null;
    if (uninstallButton) uninstallButton.onclick = null;
    if (launchButton) launchButton.onclick = null;

    if (currentResource.isInstalled === true) {
        if (installButton) installButton.style.display = 'none';
        if (uninstallButton) {
            uninstallButton.style.display = ''; // Rendre visible.
            uninstallButton.onclick = () => sendAction('uninstall', packageName);
        }
        if (launchButton) {
            launchButton.style.display = ''; // Rendre visible.
            launchButton.onclick = () => sendAction('launch', packageName);
        }
    } else if (currentResource.isInstalled === false) {
        if (installButton) {
            installButton.style.display = ''; // Rendre visible.
            installButton.onclick = () => sendAction('install', packageName);
        }
        if (uninstallButton) uninstallButton.style.display = 'none';
        if (launchButton) launchButton.style.display = 'none';
    } else { // 'unknown' ou autre erreur.
        console.warn(`État d'installation inconnu pour ${packageName}. Les boutons d'action sont cachés.`);
        if (installButton) installButton.style.display = 'none';
        if (uninstallButton) uninstallButton.style.display = 'none';
        if (launchButton) launchButton.style.display = 'none';
    }
}