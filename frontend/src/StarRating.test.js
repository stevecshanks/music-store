import React from 'react';
import {configure, shallow} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import StarRating from './StarRating';

configure({adapter: new Adapter()});

const starsIn = (rating) => rating.find('.rating-star')

const highlighted = (stars) => stars.find('.selected')

const starRatingFor = (album, rateAlbum = null) => shallow(<StarRating album={album} rateAlbum={rateAlbum} />)

const albumWithRating = (rating) => ({rating: rating})

it('renders the correct number of stars when not rated', () => {
  expect(
    starsIn(starRatingFor(albumWithRating(null)))
  ).toHaveLength(5)
})

it('renders the correct number of stars when rated', () => {
  expect(
    starsIn(starRatingFor(albumWithRating(5)))
  ).toHaveLength(5)
})

it('does not highlight any stars when not rated', () => {
  expect(
    highlighted(starsIn(starRatingFor(albumWithRating(null))))
  ).toHaveLength(0)
})

it('highlights correct number of stars when rated', () => {
  expect(
    highlighted(starsIn(starRatingFor(albumWithRating(3))))
  ).toHaveLength(3)
})

it('highlights all stars when album has maximum rating', () => {
  expect(
    highlighted(starsIn(starRatingFor(albumWithRating(5))))
  ).toHaveLength(5)
})

it('rates album correctly when clicked', () => {
  const album = albumWithRating(null)
  const rateAlbum = jest.fn()
  starsIn(starRatingFor(album, rateAlbum)).first().simulate('click')
  expect(rateAlbum).toHaveBeenCalledWith(album, 5)
})
