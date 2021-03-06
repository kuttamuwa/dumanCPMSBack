"""

Mezarlık..
"""


def analyze_kar(self):
    """
    Kar sütunu olursa...
    %0-5	15
    %5-10	10
    %10-15	7
    %15-20	5
    %20 ve üzeri	3

    """
    pnt_df = self.get_intervals_by_name('Kar', convert_df=True)
    rd = self.get_risk_dataset
    profit = rd.profit
    pts = self.get_points_from_value(profit, pnt_df)
    saved_pts = self.set_risk_points_object(risk_dataset=rd, variable='Kar',
                                            calculated_pts=pts)
    return saved_pts


