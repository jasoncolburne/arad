import { Link } from "react-router-dom";
import { Navigation } from "../../administration/Navigation";

import "./index.css"

const Header = () => {
  return (
    <header className="header">
      <div className="left">
        {/* TODO: when not an admin, don't display this */}
        <Navigation />
      </div>
      <div className="right">
        <Link to='/passphrase'>address@domain.name</Link>
      </div>
    </header>
  )
}

export { Header };