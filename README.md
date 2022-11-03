# qB-IPT

## Notice

This project has been discontinued in favor of [Jackett](https://github.com/Jackett/Jackett). Jackett supports IPTorrents [out-of-the-box](https://github.com/Jackett/Jackett/blob/master/src/Jackett.Common/Indexers/IPTorrents.cs). Here are [qBittorrent's instructions](https://github.com/qbittorrent/search-plugins/wiki/How-to-configure-Jackett-plugin) to configure Jackett in qBittorrent.

## Links

Project: <https://sr.ht/~txtsd/qB-IPT/> <br>
Sources: <https://sr.ht/~txtsd/qB-IPT/sources> <br>
Ticket Tracker: <https://todo.sr.ht/~txtsd/qB-IPT> <br>
Mailing Lists: <https://lists.sr.ht/~txtsd/qB-IPT> <br>

Mirrors: <br>
[Codeberg](https://codeberg.org/txtsd/qB-IPT) <br>
[NotABug](https://notabug.org/txtsd/qB-IPT) <br>
[GitLab](https://gitlab.com/txtsd/qb-ipt) <br>
[GitHub](https://github.com/txtsd/qB-IPT) <br>
[Bitbucket](https://bitbucket.org/txtsd/qb-ipt) <br>

If sourcehut is not feasible, contribution is welcome from across mirrors.

## Installation

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
So if your username is `herp` and your password is `derp` these lines should read:

```
    ...
    # SET THESE VALUES
    #
    username = "herp"
    password = "derp"
    ...
```

After you've done this you can add this plugin to qBittorrent by going:
 Search tab -> Plugins -> Install a new one -> Selecting the `iptorrents.py` file.

Or by manually copying the `iptorrents.py` to the following location:
  * Linux: `~/.local/share/data/qBittorrent/nova/engines/iptorrents.py`
  * Mac: `~/Library/Application Support/qBittorrent/nova/engines/iptorrents.py`
  * Windows: `C:\Documents and Settings\username\Local Settings\Application Data\qBittorrent\nova\engines\iptorrents.py`
