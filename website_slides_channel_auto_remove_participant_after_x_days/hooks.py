def post_init_hook(env):
    """Start the access period of existing memberships from their creation,
    which is what the auto-remove cron counted from before joined_date.
    The 17.0.1.0.1 migration does the same on module update."""
    env.cr.execute(
        """
        UPDATE slide_channel_partner
        SET joined_date = create_date
        WHERE joined_date IS NULL
        """
    )
