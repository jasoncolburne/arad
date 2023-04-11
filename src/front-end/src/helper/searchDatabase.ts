import { Article } from "../mock-data-util/mock-interface";
// temp sorting helper, makes hash map, no copies, too slow though

function buildMap(data: Article[]): { [key: string]: Article[] } {
  const map: { [key: string]: Article[] } = {};

  for (const article of data) {
    const keys = Object.keys(article);

    for (const key of keys) {
      const value = article[key]?.toString()?.toLowerCase() ?? "";
      const words = value.split(" ");

      for (const word of words) {
        if (word.length) {
          if (!map[word]) {
            map[word] = [];
          }

          map[word].push(article);
        }
      }
    }
  }
  return map;
}
/**
 * returns all articles containing matching character from any field sorted by title relevance first.
 *  @param {Article[]} data
 *  @param {string} searchTerm
 *  @return {Object} results
 * 
 */
export function searchArray(data: Article[], searchTerm: string | undefined): Article[] {
  const map = buildMap(data);
  const resultsMap: { [key: string]: Article } = {};

  const searchArray = searchTerm?.toLowerCase().split(" ");
  if (!searchArray) {
    return [];
  }
  for (const s of searchArray) {
    const term = s;
    if (!term.length) {
      continue;
    }
    const keys = Object.keys(map);

    for (const key of keys) {
      const value = key.toLowerCase();
      
      if (value.includes(term)) {
        const articles = map[key];

        for (const article of articles) {
          resultsMap[article._id] = article;
        }
      }
    }
  }
  const results = Object.values(resultsMap);

  results.sort((a, b) => {
    const aTitle = a.title.toLowerCase();
    const bTitle = b.title.toLowerCase();
    // by title relevance first
    if (aTitle.includes(searchTerm!) && !bTitle.includes(searchTerm!)) {
      return -1;
    }
    if (!aTitle.includes(searchTerm!) && bTitle.includes(searchTerm!)) {
      return 1;
    }
    if (aTitle.indexOf(searchTerm!) < bTitle.indexOf(searchTerm!)) {
      return -1;
    }
    return 1;
  });
  return results;
}