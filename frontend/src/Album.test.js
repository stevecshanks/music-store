import React from 'react';
import {configure, shallow} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import Album from './Album';

configure({adapter: new Adapter()});

const anAlbum = (overrides) => {
  const defaults = {
    artist: 'an artist',
    name: 'an album name',
    cover_image_url: '',
    bandcamp_url: '',
  }
  return {...defaults, ...overrides}
}

const anUnpurchasedAlbum = () => anAlbum({purchased: false})

const aPurchasedAlbum = () => anAlbum({purchased: true})

const albumWrapper = (album, purchaseAlbum, downloadAlbum) => shallow(
  <Album album={album} purchaseAlbum={purchaseAlbum} downloadAlbum={downloadAlbum}/>
)

const clickActionButtonOn = (wrapper) => {
  const mockEvent = {target: {}}
  wrapper.find('button').first().simulate('click', mockEvent)
}

it('allows unpurchased album to be purchased', () => {
  const album = anUnpurchasedAlbum()
  const purchaseAlbum = jest.fn()
  const downloadAlbum = jest.fn()

  clickActionButtonOn(albumWrapper(album, purchaseAlbum, downloadAlbum))

  expect(purchaseAlbum).toHaveBeenCalledWith(album)
  expect(downloadAlbum).not.toHaveBeenCalled()
})

it('allows purchased album to be downloaded', () => {
  const purchaseAlbum = jest.fn()
  const downloadAlbum = jest.fn()

  clickActionButtonOn(albumWrapper(aPurchasedAlbum(), purchaseAlbum, downloadAlbum))

  expect(purchaseAlbum).not.toHaveBeenCalled()
  expect(downloadAlbum).toHaveBeenCalled()
})
