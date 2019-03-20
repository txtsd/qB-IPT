qB-IPT
======

Installation
------------

Because IPTorrents requires an account, this plugin requires a bit more work than most.

1. You will need an [IPTorrents account](https://iptorrents.com) (You can only acquire one via an invite)
2. You will need to put your login information directly into the [plugin file](iptorrents.py):

You can do this by editing these specific lines (41:42).

```
    # Login information ######################################################
    #
    # SET THESE VALUES!!
    #
    username = "username"
    password = "password"
    ##########################################################################
    ...
```

Now replace the "username" and "password" with *your* username and password, surrounded by quotation marks.
So if your username is `foobar` and your password is `bazqux` these lines should read:

```
    ...
    # SET THESE VALUES
    #
    username = "foobar"
    password = "bazqux"
    ...
```

After you've done this you can add this plugin to qBittorrent by going:
 Search tab -> Plugins -> Install a new one -> Selecting the `iptorrents.py` file.

Or by manually copying the `iptorrents.py` to the following location:
  * Linux: `~/.local/share/data/qBittorrent/nova/engines/iptorrents.py`
  * Mac: `~/Library/Application Support/qBittorrent/nova/engines/iptorrents.py`
  * Windows: `C:\Documents and Settings\username\Local Settings\Application Data\qBittorrent\nova\engines\iptorrents.py`
