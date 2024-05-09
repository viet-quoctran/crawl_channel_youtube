import sys
import io

# Thay đổi mã hóa toàn cục cho stdout để hỗ trợ UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='ignore')
API_KEY = 'AIzaSyBUW8KicIHrWyQ_KCQ67DwYeve5WBFwPOI'
DEFAULT_COUNTRY = 'JP'
DEFAULT_QUERY = 'フットボール'