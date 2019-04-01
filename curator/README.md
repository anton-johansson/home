# Curator

Curator is a tool that is used to clean up old Elasticsearch indices.


## Schedule

The container itself dies after an execution. So we need a cron job that starts it. Add the following to the crontab using `crontab -e`:

```
0 2 * * * docker start curator
```
