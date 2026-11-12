# (str) Title of your application
title = ArmanChat

# (str) Package name
package.name = armanchat

# (str) Package domain (needed for android packaging)
package.domain = org.armanchat

# (list) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,pyrebase,requests,urllib3,certifi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
