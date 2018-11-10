import React, {Component} from "react";

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

export default StarRating;
