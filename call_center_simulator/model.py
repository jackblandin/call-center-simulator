class LeadScoringModel:

    def __init__(self):
        """Abstract base class for a lead scoring model.
        """
        raise Exception("Can't instantiate base class.")

    def predict(self):
        raise NotImplementedError()


class NaiveLeadScoringModel(LeadScoringModel):

    def __init__(self):
        """Uninformative (naive) model predicting LTV of a lead.
        """
        pass

    def predict(self, lead):
        """Returns 0 everytime.

        Parameters
        ----------
        lead : Lead
            Lead to predict on.

        Returns
        -------
        float
            Predicted LTV.
        """
        return 0


class PerfectLeadScoringModel(LeadScoringModel):

    def __init__(self):
        """Predicts the value of a lead perfectly, returning lead's actual LTV.
        """
        pass

    def predict(self, lead):
        """Returns the lead's actual LTV.

        Parameters
        ----------
        lead : Lead
            Lead to predict on.

        Returns
        -------
        float
            Lead's LTV.
        """
        return lead.ltv
