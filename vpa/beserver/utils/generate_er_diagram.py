from vpa.beserver.extensions import db
from vpa.beserver.models import User, Role, Parking_Lot, Parking_Spot, Reservation  # import your models

from eralchemy2 import render_er

# Generate ER diagram
output_file = './er_diagram/er_diagram.png'

try:
    render_er(db.Model, output_file)
    print(f"✅ ER diagram generated successfully: {output_file}")
except Exception as e:
    print(f"❌ Error generating ER diagram: {e}")
