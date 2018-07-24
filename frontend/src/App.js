import React, {Component} from 'react';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.setAlbumFilter = this.setAlbumFilter.bind(this)
    this.purchaseAlbum = this.purchaseAlbum.bind(this)
    this.rateAlbum = this.rateAlbum.bind(this)
    this.state = {
      albums: [],
      albumFilter: null
    }
  }

  componentDidMount() {
    this.callApi()
      .then(response => this.setState({
        albums: response,
      }))
      .catch(error => console.log(error));
  }

  callApi = async () => {
    const response = await fetch('/api/albums');
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body)
    }

    return body;
  }

  setAlbumFilter(albumFilter) {
    this.setState({albumFilter: albumFilter})
  }

  purchaseAlbum = async (album) => {
    const response = await fetch('/api/albums/' + album.id + '/buy');
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body)
    }

    this.setState((state, props) => {
      const index = state.albums.findIndex((element, index, array) => element.id === album.id)
      state.albums[index] = body
      return state
    });
  }

  rateAlbum = async (album, rating) => {
    const response = await fetch(
      '/api/albums/' + album.id + '/rate',
      {
        method: 'PUT',
        body: JSON.stringify({rating: rating}),
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body)
    }

    this.setState((state, props) => {
      const index = state.albums.findIndex((element, index, array) => element.id === album.id)
      state.albums[index] = body
      return state
    });
  }

  render() {
    return (
      <div>
        <Header/>
        <main role="main">
          <div className="album py-2 bg-light">
            <div className="container">
              <FlashMessages/>
              <AlbumList albums={this.state.albums} albumFilter={this.state.albumFilter}
                         setAlbumFilter={this.setAlbumFilter} purchaseAlbum={this.purchaseAlbum}
                         rateAlbum={this.rateAlbum}/>
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
        <div className="collapse bg-dark" id="navbarHeader">
          <div className="container">
            <div className="row">
              <div className="col-sm-8 col-md-7 py-4">
                <h4 className="text-white">About</h4>
                <p className="text-muted">A simple music store app to play around with Flask</p>
              </div>
            </div>
          </div>
        </div>
        <div className="navbar navbar-dark bg-dark box-shadow">
          <div className="container d-flex justify-content-between">
            <a href="/" className="navbar-brand d-flex align-items-center">
              <strong>Music Store</strong>
            </a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarHeader"
                    aria-controls="navbarHeader" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"/>
            </button>
          </div>
        </div>
      </header>
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
      <Album key={album.id} album={album} purchaseAlbum={this.props.purchaseAlbum} rateAlbum={this.props.rateAlbum}/>
    ));
    return (
      <div>
        <AlbumFilters setAlbumFilter={this.props.setAlbumFilter}/>
        <div className="row">
          {albums}
        </div>
      </div>
    );
  }
}

class FlashMessages extends Component {
  render() {
    return (
      <div className="alert alert-warning" role="alert">a flash message</div>
    );
  }
}

class AlbumFilters extends Component {
  state = {
    activeFilter: 'All'
  }

  updateFilter(e, filter) {
    this.props.setAlbumFilter(filter)
    this.setState({activeFilter: e.target.innerHTML})
  };

  render() {
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <ul className="navbar-nav mr-auto">
          <FilterButton activeFilter={this.state.activeFilter} name='All'
                        handleClick={(e) => this.updateFilter(e, null)}/>
          <FilterButton activeFilter={this.state.activeFilter} name='Purchased'
                        handleClick={(e) => this.updateFilter(e, (album) => album.purchased)}/>
          <FilterButton activeFilter={this.state.activeFilter} name='Unpurchased'
                        handleClick={(e) => this.updateFilter(e, (album) => !album.purchased)}/>
        </ul>
      </nav>
    );
  }
}

class FilterButton extends Component {
  render() {
    const active = this.props.activeFilter === this.props.name ? 'active' : '';
    const className = 'nav-link ' + active;
    return (
      <li className="nav-item ">
        <a href="#" className={className} onClick={this.props.handleClick}>{this.props.name}</a>
      </li>
    )
  }
}

class Album extends Component {
  constructor(props) {
    super(props);
    this.handlePurchase = this.handlePurchase.bind(this)
  }

  handlePurchase() {
    this.props.purchaseAlbum(this.props.album)
  }

  render() {
    const album = this.props.album;
    let actionButton;
    if (album.purchased){
      actionButton = <a href="#" className="btn btn-sm btn-outline-secondary">Download</a>
    } else {
      actionButton = <a href="#" className="btn btn-sm btn-outline-secondary" onClick={this.handlePurchase}>Buy</a>
    }
    return (
      <div className="col-md-4">
        <div className="card mb-4 box-shadow">
          <img className="card-img-top" src={album.cover_image_url} alt="Card image cap"/>
          <div className="card-body">
            <p className="card-text">
              <StarRating album={album} rateAlbum={this.props.rateAlbum}/>
              <h5>{album.artist}</h5>
              {album.name}
            </p>
            <div className="d-flex justify-content-between align-items-center">
              <div className="btn-group">
                {actionButton}
                <a href={album.bandcamp_url} className="btn btn-sm btn-outline-secondary">Bandcamp</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

class StarRating extends Component {
  constructor(props) {
    super(props);
    this.handleRating = this.handleRating.bind(this)
  }

  handleRating(rating) {
    this.props.rateAlbum(this.props.album, rating)
  }

  render() {
    const stars = [5, 4, 3, 2, 1].map((n) => {
        const selected = n <= this.props.album.rating ? 'selected' : '';
        const className = "rating-star " + selected;
        return <a key={n} href="#" className={className} onClick={() => this.handleRating(n)}>&#9733;</a>
      }
    );

    return (
      <div className="rating">
        {stars}
      </div>
    );
  }
}

export default App;
