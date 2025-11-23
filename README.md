# Key-Value Store with Memtable and SSTables

A key-value store built with Python. It uses an in-memory memtable for fast writes and persists data to SSTables on disk when the memtable reaches a limit. SSTables are tracked in a manifest to allow retrieval from newest to oldest.
