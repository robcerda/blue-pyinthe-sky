import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bluepyinthesky.server import Server

print(Server().getAccountInviteCodes(include_used=True
                                     ,create_available=True))