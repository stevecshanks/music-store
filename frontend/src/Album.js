import React, {Component} from "react";

import StarRating from './StarRating';

class Album extends Component {
  constructor(props) {
    super(props);
    this.handlePurchase = this.handlePurchase.bind(this)
    this.handleDownload = this.handleDownload.bind(this)
  }

  handlePurchase() {
    this.props.purchaseAlbum(this.props.album)
  }

  handleDownload(e) {
    this.props.downloadAlbum(this.props.album)
    e.target.innerText = 'Added to Downloads'
    e.target.disabled = true
  }

  render() {
    const album = this.props.album;
    let actionButton;
    if (album.purchased) {
      actionButton = <button className="btn btn-sm btn-outline-secondary"
                             onClick={(e) => this.handleDownload(e)}>Download</button>
    } else {
      actionButton = <button className="btn btn-sm btn-outline-secondary" onClick={this.handlePurchase}>Buy</button>
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

export default Album;
