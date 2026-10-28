def migrate(cr, version):
    """Start the access period of existing memberships from their creation,
    which is what the auto-remove cron counted from before joined_date.
    """
    cr.execute(
        """
        UPDATE slide_channel_partner
        SET joined_date = create_date
        WHERE joined_date IS NULL
        """
    )
