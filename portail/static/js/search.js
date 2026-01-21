// search.js
// Ce fichier contient la logique de filtrage des ressources par terme de recherche.
// Cette fonction manipule des tableaux de ressources et retourne les résultats.

/**
 * Filtre un tableau de ressources en fonction d'un terme de recherche.
 * La recherche est effectuée sur le titre et la description des ressources.
 * Cette fonction ne manipule PAS le DOM.
 * @param {Array<Object>} ressourcesArray - Le tableau de ressources à filtrer. Chaque objet doit avoir des propriétés 'titre' et 'description'.
 * @param {string} searchTerm - Le terme de recherche.
 * @returns {Array<Object>} - Une nouvelle copie du tableau de ressources filtré.
 */
export function rechercher(ressourcesArray, searchTerm) {
    const lowerTerm = searchTerm.toLowerCase().trim();
    // Si le terme de recherche est vide, retourne toutes les ressources.
    if (!lowerTerm) {
        return ressourcesArray;
    }
    // Filtre les ressources dont le titre ou la description inclut le terme de recherche.
    return ressourcesArray.filter(r =>
        r.title.toLowerCase().includes(lowerTerm) ||
        r.short_desc.toLowerCase().includes(lowerTerm)
    );
}
