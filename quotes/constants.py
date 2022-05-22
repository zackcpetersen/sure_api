from decimal import Decimal


VOLCANIC_STATE_FEE = Decimal(0.25)
PREV_POLICY_CANCELLED_FEE = Decimal(0.15)
NEVER_CANCELLED_DISCOUNT = Decimal(-0.1)
PROPERTY_OWNER_DISCOUNT = Decimal(-0.2)

STATE_CHOICES = (
    ("AK", "Alaska"),
    ("AL", "Alabama"),
    ("AR", "Arkansas"),
    ("AS", "American Samoa"),
    ("AZ", "Arizona"),
    ("CA", "California"),
    ("CM", "Northern Mariana Islands"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DC", "District of Columbia"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("GU", "Guam"),
    ("HI", "Hawaii"),
    ("IA", "Iowa"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("MA", "Massachusetts"),
    ("MD", "Maryland"),
    ("ME", "Maine"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MO", "Missouri"),
    ("MS", "Mississippi"),
    ("MT", "Montana"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("NE", "Nebraska"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NV", "Nevada"),
    ("NY", "New York"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("PR", "Puerto Rico"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TT", "Trust Territories"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VA", "Virginia"),
    ("VI", "Virgin Islands"),
    ("VT", "Vermont"),
    ("WA", "Washington"),
    ("WI", "Wisconsin"),
    ("WV", "West Virginia"),
    ("WY", "Wyoming")
)

VOLCANIC_STATES = ["AK", "AZ", "CA", "CO", "HI", "ID", "NV", "NM", "OR", "UT", "WA", "WY"]
