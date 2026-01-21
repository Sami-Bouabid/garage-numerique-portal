// sort.js
// Ce fichier contient les fonctions de tri et de filtrage des ressources par titre et par catégorie.

/**
 * Trie un tableau de ressources par titre dans l'ordre spécifié (ascendant ou descendant).
 * @param {Array<Object>} ressourcesArray - Tableau de ressources avec une propriété 'title'.
 * @param {string} order - 'asc' pour ascendant, 'desc' pour descendant.
 * @returns {Array<Object>} - Une copie triée du tableau.
 */

export function trierRessources(ressourcesArray, order) {
    const sortedRessources = [...ressourcesArray];
    if (order === "asc") {
      sortedRessources.sort((a, b) => a.title.localeCompare(b.title));
    } else if (order === "desc") {
      sortedRessources.sort((a, b) => b.title.localeCompare(a.title));
    }
    return sortedRessources;
  }
  
  /**
   * Filtre un tableau de ressources selon une catégorie choisie.
   * Si aucune catégorie n'est spécifiée, retourne toutes les catégories uniques disponibles.
   * @param {Array<Object>} ressourcesArray - Tableau de ressources avec une propriété 'subjects'.
   * @param {string} category - La catégorie à filtrer (ou chaîne vide pour extraire toutes les catégories).
   * @returns {Array<Object>|Array<string>} - Ressources filtrées ou liste des catégories uniques.
   */

  export function filtrerParCategorie(ressourcesArray, category) {
    // Si aucune catégorie spécifiée, extraire toutes les catégories uniques
    if (!category || category.trim() === "") {
      const uniqueCategories = new Set();
      
      ressourcesArray.forEach(ressource => {
        try {
          // Parse les subjects (JSON string vers array)
          const subjectsArray = Array.isArray(ressource.subjects) 
            ? ressource.subjects 
            : JSON.parse(ressource.subjects.replace(/'/g, '"'));
          
          subjectsArray.forEach(subject => {
            if (subject && subject.trim()) {
              // Normalise : minuscules + supprime accents
              const normalized = subject.trim()
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '');
              
              // Cherche si une catégorie similaire existe déjà
              let found = false;
              for (let existing of uniqueCategories) {
                const existingNormalized = existing
                  .toLowerCase()
                  .normalize('NFD')
                  .replace(/[\u0300-\u036f]/g, '');
                
                if (normalized === existingNormalized) {
                  found = true;
                  break;
                }
              }
              
              // Ajoute seulement si pas trouvé de similaire
              if (!found) {
                uniqueCategories.add(subject.trim());
              }
            }
          });
        } catch (e) {
          console.warn("Erreur parsing subjects:", ressource.subjects, e);
        }
      });
      
      return Array.from(uniqueCategories).sort();
    }
    
    // Filtrer par catégorie spécifique
    const categoryNormalized = category.trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
    
    return ressourcesArray.filter(ressource => {
      try {
        const subjectsArray = Array.isArray(ressource.subjects)
          ? ressource.subjects
          : JSON.parse(ressource.subjects.replace(/'/g, '"'));
        
        return subjectsArray.some(subject => {
          const subjectNormalized = subject.trim()
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '');
          
          return subjectNormalized === categoryNormalized;
        });
      } catch (e) {
        console.warn("Erreur parsing subjects:", ressource.subjects, e);
        return false;
      }
    });
  }