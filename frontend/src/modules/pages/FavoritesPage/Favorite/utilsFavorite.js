export const handleCheckboxFavorite = (
  e,
  selectedFavoritesIds,
  setSelectedFavoritesIds,
) => {
  let value = parseInt(e.target.value);

  if (e.target.checked) {
    setSelectedFavoritesIds([...selectedFavoritesIds, value]);
  } else {
    setSelectedFavoritesIds((prevState) => {
      return prevState.filter((id) => {
        return id !== value;
      });
    });
  }
};

export const pluralize = (forms, number) => {
  let formIndex;

  if (number % 10 === 1 && number % 100 !== 11) {
    formIndex = 0;
  } else if (
    number % 10 >= 2 &&
    number % 10 <= 4 &&
    (number % 100 < 10 || number % 100 >= 20)
  ) {
    formIndex = 1;
  } else {
    formIndex = 2;
  }

  return forms[formIndex];
};
