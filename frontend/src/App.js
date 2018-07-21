import React, {Component} from 'react';
import './App.css';

class App extends Component {
  state = {
    albums: []
  };

  componentDidMount() {
    this.callApi()
      .then(response => this.setState({albums: response}))
      .catch(error => console.log(error));
  }

  callApi = async () => {
    const response = await fetch('/api/albums');
    const body = await response.json();

    if (response.status !== 200) {
      throw Error(body)
    }

    return body
  }

  render() {
    return (
      <div>
        <Header/>
        <main role="main">
          <div className="album py-2 bg-light">
            <div className="container">
              <FlashMessages/>
              <AlbumList albums={this.state.albums}/>
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
    const albums = this.props.albums.map((album =>
      <Album key={album.id} album={album}/>
    ));
    return (
      <div>
        <AlbumFilters/>
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
  render() {
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item active"><a href="#" className="nav-link">All</a></li>
          <li className="nav-item"><a href="#" className="nav-link">Purchased</a></li>
          <li className="nav-item "><a href="#" className="nav-link">Unpurchased</a></li>
        </ul>
      </nav>
    );
  }
}

class Album extends Component {
  render() {
    const album = this.props.album;
    return (
      <div className="col-md-4">
        <div className="card mb-4 box-shadow">
          <img className="card-img-top" src={album.cover_image_url} alt="Card image cap"/>
          <div className="card-body">
            <p className="card-text">
              <StarRating rating={album.rating}/>
              <h5>{album.artist}</h5>
              {album.name}
            </p>
            <div className="d-flex justify-content-between align-items-center">
              <div className="btn-group">
                <a href="#" className="btn btn-sm btn-outline-secondary">Buy</a>
                <a href="#" className="btn btn-sm btn-outline-secondary">Download</a>
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
  render() {
    const stars = [5, 4, 3, 2, 1].map((n) => {
        const selected = n <= this.props.rating ? 'selected' : '';
        const className = "rating-star " + selected;
        return <a href="#" className={className}>&#9733;</a>
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
