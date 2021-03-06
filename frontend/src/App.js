import React, {Component} from 'react';
import Album from './Album';
import './App.css';

import io from 'socket.io-client';

const uuid = require('uuid/v4')

const FILTER_ALL_ALBUMS = null
const FILTER_PURCHASED_ALBUMS = (album) => album.purchased
const FILTER_UNPURCHASED_ALBUMS = (album) => !album.purchased

class App extends Component {
  constructor(props) {
    super(props);
    this.setAlbumFilter = this.setAlbumFilter.bind(this)
    this.purchaseAlbum = this.purchaseAlbum.bind(this)
    this.downloadAlbum = this.downloadAlbum.bind(this)
    this.markDownloadAsReady = this.markDownloadAsReady.bind(this)
    this.rateAlbum = this.rateAlbum.bind(this)
    this.dismissFlashMessage = this.dismissFlashMessage.bind(this)
    this.state = {
      albums: [],
      albumFilter: FILTER_ALL_ALBUMS,
      messages: [],
      downloads: [],
    }
    this.socket = io();
  }

  componentDidMount() {
    this.listAlbums()
      .then(response => this.setState({
        albums: response,
      }))
      .catch(error => console.log(error));

    this.socket.on('download ready', (data) => this.markDownloadAsReady(data))
  }

  callApi = async (endpoint, method = 'GET', json = null) => {
    let init = {method: method}
    if (json) {
      init['body'] = JSON.stringify(json)
      init['headers'] = {'Content-Type': 'application/json'}
    }

    const response = await fetch(endpoint, init);
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body['error'])
    }

    return body;
  }

  listAlbums = async () => {
    return this.callApi('/api/albums')
  }

  purchaseAlbum = async (album) => {
    try {
      const response = await this.callApi('/api/albums/' + album.id + '/purchase', 'POST')

      this.updateAlbumState(album, response)
      this.addFlashMessage('success', 'Album purchased successfully!')
      this.setAlbumFilter(FILTER_PURCHASED_ALBUMS)
    } catch (err) {
      this.addFlashMessage('danger', err.message)
    }
  }

  downloadAlbum = async (album) => {
    try {
      const response = await this.callApi('/api/albums/' + album.id + '/downloads', 'POST')

      this.setState((state, props) => {
        const download = {
          id: response['id'],
          album: album,
          status: 'pending',
          url: '#',
        }
        return {downloads: [...state.downloads, download]}
      });
    } catch (err) {
      this.addFlashMessage('danger', err.message)
    }
  }

  markDownloadAsReady(download) {
    this.setState((state, props) => {
      const index = state.downloads.findIndex((element, index, array) => element.id === download.id)
      if (index !== -1) {
        state.downloads[index].status = 'ready'
        state.downloads[index].url = download.url
      }
      return state
    });
  }

  rateAlbum = async (album, rating) => {
    try {
      const response = await this.callApi('/api/albums/' + album.id + '/rating', 'PUT', {rating: rating})

      this.updateAlbumState(album, response)
    } catch (err) {
      this.addFlashMessage('danger', err.message)
    }
  }

  updateAlbumState(oldAlbum, updatedAlbum) {
    this.setState((state, props) => {
      const index = state.albums.findIndex((element, index, array) => element.id === oldAlbum.id)
      state.albums[index] = updatedAlbum
      return state
    });
  }

  addFlashMessage(type, text) {
    this.setState((state, props) => {
      const message = {
        id: uuid(),
        type: type,
        text: text
      }
      return {messages: [...state.messages, message]}
    });
  }

  dismissFlashMessage(message) {
    this.setState((state, props) => {
      return {
        messages: state.messages.filter((m) => m.id !== message.id)
      }
    });
  }

  setAlbumFilter(albumFilter) {
    this.setState({albumFilter: albumFilter})
  }

  render() {
    return (
      <div>
        <Header downloads={this.state.downloads}/>
        <main role="main">
          <div className="album py-2 bg-light">
            <div className="container">
              <FlashMessages messages={this.state.messages} dismissMessage={this.dismissFlashMessage}/>
              <AlbumList albums={this.state.albums} albumFilter={this.state.albumFilter}
                         setAlbumFilter={this.setAlbumFilter} purchaseAlbum={this.purchaseAlbum}
                         downloadAlbum={this.downloadAlbum} rateAlbum={this.rateAlbum}/>
            </div>
          </div>
        </main>
      </div>
    );
  }
}

class Header extends Component {
  render() {
    return (
      <header>
        <div className="navbar navbar-expand-lg navbar-dark bg-dark box-shadow">
          <div className="container d-flex justify-content-between">
            <a href="/" className="navbar-brand d-flex align-items-center">
              <strong>Music Store</strong>
            </a>
            <div className="collapse navbar-collapse" id="navbarNavDropdown">
              <ul className="navbar-nav">
                <DownloadList downloads={this.props.downloads}/>
              </ul>
            </div>
          </div>
        </div>
      </header>
    );
  }
}

class DownloadList extends Component {
  render() {
    if (this.props.downloads.length === 0) {
      return ''
    }

    const downloadsToDisplay = this.props.downloads.map((download) =>
      <Download key={download.id} album={download.album} download={download}/>
    );

    const pendingDownloads = this.props.downloads.filter((download) => download.status === 'pending')
    const readyDownloads = this.props.downloads.filter((download) => download.status === 'ready')

    return (
      <li className="nav-item dropdown">
        <a className="nav-link dropdown-toggle" href="#" id="downloadListMenuLink" data-toggle="dropdown"
           aria-haspopup="true" aria-expanded="false">
          Downloads
          <DownloadCountBadge status='ready' downloads={readyDownloads}/>
          <DownloadCountBadge status='pending' downloads={pendingDownloads}/>
        </a>
        <div className="dropdown-menu" aria-labelledby="downloadListMenuLink">
          {downloadsToDisplay}
        </div>
      </li>
    );
  }
}

class DownloadStatusBadge extends Component {
  render() {
    const badge_type = this.props.status === 'ready' ? 'success' : 'warning'
    const badge_class = "badge badge-" + badge_type

    return (
      <span className={badge_class}>{this.props.text}</span>
    );
  }
}

class DownloadCountBadge extends Component {
  render() {
    if (this.props.downloads.length === 0) {
      return ''
    }

    return (
      <span>
        &nbsp;<DownloadStatusBadge status={this.props.status} text={this.props.downloads.length}/>
      </span>
    );
  }
}

class Download extends Component {
  render() {
    const album = this.props.album;
    const download = this.props.download
    const capitalised_status = download.status.charAt(0).toUpperCase() + download.status.substr(1)

    return (
      <a className="dropdown-item" href={download.url}>
        <DownloadStatusBadge status={download.status} text={capitalised_status}/> {album.artist} - {album.name}
      </a>
    );
  }
}

class AlbumList extends Component {
  render() {
    let albumsToDisplay = this.props.albums;
    if (this.props.albumFilter) {
      albumsToDisplay = albumsToDisplay.filter(this.props.albumFilter)
    }
    const albums = albumsToDisplay.map((album =>
        <Album key={album.id} album={album} purchaseAlbum={this.props.purchaseAlbum}
               downloadAlbum={this.props.downloadAlbum} rateAlbum={this.props.rateAlbum}/>
    ));
    return (
      <div>
        <AlbumFilters albumFilter={this.props.albumFilter} setAlbumFilter={this.props.setAlbumFilter}/>
        <div className="row">
          {albums}
        </div>
      </div>
    );
  }
}

class FlashMessages extends Component {
  render() {
    return this.props.messages.map((message =>
        <FlashMessage key={message.id} message={message} dismissMessage={this.props.dismissMessage}/>
    ));
  }
}

class FlashMessage extends Component {
  render() {
    const message = this.props.message
    const className = "alert alert-dismissible fade show alert-" + message.type;
    return (
      <div className={className} role="alert">{message.text}
        <button type="button" className="close" aria-label="Close" onClick={() => this.props.dismissMessage(message)}>
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    )
  }
}

class AlbumFilters extends Component {
  render() {
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <ul className="navbar-nav mr-auto">
          <FilterButton filter={FILTER_ALL_ALBUMS} activeFilter={this.props.albumFilter} name='All'
                        handleClick={this.props.setAlbumFilter}/>
          <FilterButton filter={FILTER_PURCHASED_ALBUMS} activeFilter={this.props.albumFilter} name='Purchased'
                        handleClick={this.props.setAlbumFilter}/>
          <FilterButton filter={FILTER_UNPURCHASED_ALBUMS} activeFilter={this.props.albumFilter} name='Unpurchased'
                        handleClick={this.props.setAlbumFilter}/>
        </ul>
      </nav>
    );
  }
}

class FilterButton extends Component {
  render() {
    const active = this.props.activeFilter === this.props.filter ? 'active' : '';
    const className = 'nav-link ' + active;
    return (
      <li className="nav-item ">
        <a href="#" className={className}
           onClick={() => this.props.handleClick(this.props.filter)}>{this.props.name}</a>
      </li>
    )
  }
}

export default App;
