from extensions import app

import filters  # noqa: F401
import models  # noqa: F401
import errors  # noqa: F401
import routes.main  # noqa: F401
import routes.venues  # noqa: F401
import routes.artists  # noqa: F401
import routes.shows  # noqa: F401

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
